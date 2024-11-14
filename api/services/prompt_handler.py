# prompt_handler.py
from api.config import MODEL_NAME, AWS_REGION, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID

from langchain_aws import ChatBedrock
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain  # Ensure you have the right imports based on LangChain setup
from api.services.data_retrieval import get_sensor_data
from api.services.load_rag_data import rag_query_pipeline
import os

def generate_insight(sensor_id=None):
    """Generates insights using data retrieved from MongoDB and LangChain for analysis."""
    try:
        # Retrieve sensor data
        documents = get_sensor_data(sensor_id=sensor_id)

        if not documents:
            return "No data available for the specified sensor."
        
        # Construct the input prompt for LangChain
        template = """
        Given the following environmental data over the past week:
        {data}

        Please summarize the key trends and provide insights.
        """

        data_str = "\n".join([doc.page_content for doc in documents])

        prompt_template = PromptTemplate(input_variables=["data"], template=template)

        prompt = prompt_template.format(data=data_str)

        print(prompt)

        # Configure Amazon Bedrock LLM
        llm = ChatBedrock(model=MODEL_NAME, region=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

        print("Got here...")
        # Use the `|` operator to chain the formatted prompt to the llm
        response = (prompt_template | llm).invoke({"data": data_str})
        print(response)
        
        return response
    except Exception as e:
        return {str(e)}

def generate_rag_query_insight(query=None):
    """Generates insights using data retrieved from MongoDB and LangChain for analysis."""
    try:
        # Retrieve sensor data
        rag_response = rag_query_pipeline(query_text=query)

        if not rag_response:
            return "Apologies, I don't have an answer to that!"
        
        return rag_response
    except Exception as e:
        return {str(e)}