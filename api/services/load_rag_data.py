import json
import boto3
import os
import certifi
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import re
from datetime import datetime

# Initialize the Bedrock client (ensure your AWS credentials are properly set up)
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

load_dotenv()

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("VECTOR_DB_NAME")
COLLECTION_NAME = os.getenv("VECTOR_COLLECTION_NAME")

# MongoDB client setup
ca = certifi.where()
client = MongoClient(MONGO_URI, tlsCAFile=ca)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Function to generate embedding using Amazon Titan model
def generate_embedding(text):
    try:
        native_request = {"inputText": text}
        request = json.dumps(native_request)

        response = bedrock_client.invoke_model(
            modelId='amazon.titan-embed-text-v1',  # Titan embed text model ID
            body=request,  # Input text for embedding generation
            contentType='application/json',  # Content type for the request
            accept='application/json'  # Expected response format
        )
        
        # Parse the response to get the embedding vector
        embedding = json.loads(response['body'].read().decode('utf-8'))['embedding']
        return embedding
    except Exception as e:
        return {str(e)}

def generate_answer_with_claude(prompt):
    """
    Sends the prompt to Claude Sonnet on AWS Bedrock and returns the response.
    
    Args:
        prompt (str): The prompt text for Claude to process.
    
    Returns:
        str: The response generated by Claude.
    """
    # Prepare request payload
    try:
        request_payload = {
            "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
            "max_tokens_to_sample": 1500,
            "temperature": 0.7
        }

        # Invoke Claude Sonnet model through Bedrock
        response = bedrock_client.invoke_model(
            modelId="anthropic.claude-instant-v1",  # Specify Claude's model ID
            body=json.dumps(request_payload),
            contentType="application/json",
            accept="application/json"
        )

        # Parse response body
        response_body = json.loads(response['body'].read().decode('utf-8'))
        answer = response_body.get("completion", "").strip()

        print(answer)

        return answer
    except Exception as e:
        return {str(e)}

def get_query_results(query):
    try:
        print(f"Received query: {query}")
        
        query_embedding = generate_embedding(query)
        print(f"Generated embedding for query")
        
        extracted_date = extract_date_from_query(query)
        print(f"Extracted Date: {extracted_date}")
        
        pipeline = [
            {
                "$search": {
                    "index": "vector_search_index",  # Use the name of the search index we created
                    "knnBeta": {
                        "vector": query_embedding,
                        "path": "embedding",
                        "k": 1000
                    }
                }
            }
        ]
        
        if extracted_date:
            pipeline.append({
                "$match": {"timestamp": {"$gte": extracted_date}}
            })
        
        pipeline.extend([
            {"$sort": {"timestamp": -1}},
            {"$limit": 100},
            {
                "$project": {
                    "_id": 0,
                    "sensor_id": 1,
                    "timestamp": 1,
                    "temperature": 1,
                    "humidity": 1,
                    "AQI": 1,
                    "CO2_level": 1,
                    "id": 1,
                    "text": 1
                }
            }
        ])
        
        results = collection.aggregate(pipeline)
        
        array_of_results = list(results)
        
        print(f"Total results retrieved: {len(array_of_results)}")
        
        if array_of_results:
            print(f"Oldest result timestamp: {array_of_results[-1]['timestamp']}")
            print(f"Newest result timestamp: {array_of_results[0]['timestamp']}")
        else:
            print("No results retrieved")
        
        return array_of_results
    
    except Exception as e:
        print(f"Error in get_query_results: {str(e)}")
        return {"error": str(e)}

# Helper function to extract date/time or period from the query
def extract_date_from_query(query):
    """Extracts date from the user's query if any"""
    # Regular expression patterns for matching dates and times in the query (basic examples)
    date_patterns = [
        r'\b(\d{4}-\d{2}-\d{2})\b',  # YYYY-MM-DD format
        r'\b(\d{2}/\d{2}/\d{4})\b',  # MM/DD/YYYY format
        r'\b(on\s+\d{4}-\d{2}-\d{2})\b',  # "on YYYY-MM-DD"
        r'\b(at\s+\d{2}:\d{2}(:\d{2})?\s*(AM|PM)?)\b'  # Time format like 14:00 or 2:00 PM
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, query)
        if match:
            return match.group(0)  # Return the matched date/time/period
    
    return None  # No date/time found

def construct_prompt(user_query):
    """
    Constructs a prompt for Claude based on sensor data and user query.
    
    Args:
        user_query (str): The user's question or query regarding the sensor data.
    
    Returns:
        str: The formatted prompt for Claude.
    """
    try:
        # Extract the relevant date from the user query if any
        extracted_date = extract_date_from_query(user_query)

        # Get the context data using the user query
        context_docs = get_query_results(user_query)
        print(context_docs)
        context_string = " ".join([doc["text"] for doc in context_docs])

        # If a date is found, adjust the context accordingly
        if extracted_date:
            prompt = f"""Use the following pieces of context to answer the question at the end.
                        The question specifies a date/time, so refer to the relevant context from {extracted_date}:
                        {context_string}
                        Question: {user_query}
                    """
        else:
            # If no date is found, use the most recent context
            prompt = f"""Use the following pieces of context to answer the question at the end.
                        The question doesn't specify a date/time, so refer to the most recent context:
                        {context_string}
                        Question: {user_query}
                    """
        
        return prompt
    
    except Exception as e:
        return {"error": str(e)}


def rag_query_pipeline(query_text):
    try:
        # Step 2: Construct prompt with retrieved documents
        prompt = construct_prompt(user_query=query_text)
        
        # Step 3: Generate answer using Claude
        answer = generate_answer_with_claude(prompt)
        
        return answer
    except Exception as e:
        return {str(e)}
    
# get_query_results("how are the readings?")
