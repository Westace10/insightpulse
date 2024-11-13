# config.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# ConfigurationS
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
VECTOR_DB_NAME = os.getenv("VECTOR_DB_NAME")
VECTOR_COLLECTION_NAME = os.getenv("VECTOR_COLLECTION_NAME")
MODEL_NAME = os.getenv("MODEL_NAME")
AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

# MongoDB client setup
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
