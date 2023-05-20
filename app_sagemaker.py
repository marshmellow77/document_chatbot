import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.llms.sagemaker_endpoint import ContentHandlerBase, SagemakerEndpoint
from typing import Dict
import json
from io import StringIO
from random import randint

st.set_page_config(page_title="Document Analysis", page_icon=":robot:")
st.header("Chat with your document 📄")


class ContentHandler(ContentHandlerBase):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, prompt: str, model_kwargs: Dict) -> bytes:
        input_str = json.dumps({"prompt": prompt, "maxTokens": 100, "temperature": 0, "stopSequences": ["Human"]})
        return input_str.encode('utf-8')

    def transform_output(self, output: bytes) -> str:
        response_json = output.read()
        res = json.loads(response_json)
        ans = res['completions'][0]['data']['text']
        return ans


endpoint_name = "j2-jumbo-instruct"
content_handler = ContentHandler()


@st.cache_resource
def load_chain():
    llm = SagemakerEndpoint(
        endpoint_name=endpoint_name,
        region_name="us-east-1",
        model_kwargs={"temperature": 1e-10},
        content_handler=content_handler
    )

    memory = ConversationBufferMemory()
    chain = ConversationChain(llm=llm, memory=memory)
    return chain


chatchain = load_chain()

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
    chatchain.memory.clear()
if 'widget_key' not in st.session_state:
    st.session_state['widget_key'] = str(randint(1000, 100000000))

st.sidebar.title("Sidebar")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['widget_key'] = str(randint(1000, 100000000))
    chatchain.memory.clear()

uploaded_file = st.sidebar.file_uploader("Upload a txt file", type=["txt"], key=st.session_state['widget_key'])

response_container = st.container()
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output = chatchain(user_input)["response"]
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
    elif uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        content = stringio.read()
        content += "\nPlease confirm that you have read that file by saying 'Yes, I have read the file'"
        output = chatchain(content)["response"]
        st.session_state['past'].append("I have uploaded a file. Please confirm that you have read that file.")
        st.session_state['generated'].append(output)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
