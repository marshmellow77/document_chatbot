# document_chatbot
A repository for a document chatbot

![alt text](assets/chat.png)


## Architecture diagram for SageMaker implementation
The key advantage with this implementation is that no data ever leaves your AWS account. The model is hosted in a SageMaker endpoint in your account and all inference requests will be sent to that endpoint.
![alt text](assets/arch.png)


## How to run the application with a SageMaker Endpoint
1. Go to the [SageMaker folder](src/sagemaker)
2. Install the required packages for this application with `pip install -r requirements.txt`. To avoid conflicts with existing python dependencies, it is best to do so in a virtual environment:   
  `$python3 -m venv .venv`    
  `$source .venv/bin/activate`  
  `$pip3 install -r requirements.txt`  
3. You will need a SageMaker endpoint deployed in your account. If you don't have, one you can use this [notebook](src/sagemaker/deploy_ai21_model.ipynb) to deploy the AI21 Jurassic-2 Jumbo Instruct model in your account. Before doing that, you need to go to SageMaker Foundational Model Hub (eg. https://us-west-2.console.aws.amazon.com/sagemaker/home?region=us-west-2#/foundation-models), select the model to be deployed in your SageMaker Notebook above and click "Subscribe". You only need to do it once. Otherwise, you will get an error message during SageMaker notebook execution: "ClientError: An error occurred (ValidationException) when calling the CreateModel operation: Caller is not subscribed to the marketplace offering.". (Caution: This will spin up an ml.p4d.24xlarge instance in your account to host the model, which costs ~$30 per hour!). Alternatively you can deploy a different, smaller model into a SageMaker endpoint or use a ml.g5.48xlarge.
4. Amend the [app.py](src/sagemaker/app_sm_hf_llm.py) file so that it points to your endpoint (variable `endpoint_name`) and that it loads your AWS credentials correctly (i.e. set `credentials_profile_name` when calling the `SagemakerEndpoint` class)
5. Run the app with `streamlit run app.py`
6. Upload a text file
7. Start chatting 🤗


## Running Streamlit apps in SageMaker Studio
If you want to run Streamlit apps directly in SM Studio, you can do so with command `streamlit run <app>.py --server.port 6006`. Once the app has started you can go to `https://<YOUR_STUDIO_ID>.studio.<YOUR_REGION>.sagemaker.aws/jupyter/default/proxy/6006/` to launch the app.
