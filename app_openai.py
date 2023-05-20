import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.llms.openai import OpenAI
from io import StringIO
from random import randint
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the API key from the .env file
api_key = os.getenv('API_KEY')

st.set_page_config(page_title="Document Analysis", page_icon=":robot:")
st.header("Chat with your document 📄")


@st.cache_resource
def load_chain():
    llm = OpenAI(model_name="gpt-4", temperature=0)
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
