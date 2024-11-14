# data_retrieval.py
import certifi
from api.config import MONGO_URI, DB_NAME, COLLECTION_NAME, VECTOR_DB_NAME, VECTOR_COLLECTION_NAME

from langchain.schema import Document
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
from typing import List
from api.services.load_rag_data import generate_embedding

class MongoDBRetriever:
    def __init__(self, connection_string, database_name, collection_name):
        ca = certifi.where()
        self.client = MongoClient(connection_string, tlsCAFile=ca)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def retrieve_data(self, start_date: datetime, end_date: datetime) -> List[Document]:
        try:
            query = {
                "timestamp": {"$gte": start_date, "$lte": end_date}
            }
            results = self.collection.find(query)
            
            # Format data for LangChain
            documents = [
                Document(page_content=f"Temperature: {doc['temperature']}, Humidity: {doc['humidity']}, AQI: {doc['AQI']}, CO2_level: {doc['CO2_level']}", metadata={"timestamp": doc["timestamp"], "sensor": doc["sensor_id"]})
                for doc in results
            ]
            return documents
        except Exception as e:
            return {str(e)}
    
    def retrieve_data_for_kb(self, start_date: datetime, end_date: datetime):
        try:
            query = {
                "timestamp": {"$gte": start_date, "$lte": end_date}
            }
            # results = self.collection.find(query)
            results = self.collection.find()
            
            return results
        except Exception as e:
            return {str(e)}
    
    def retrieve_data_by_id(self, sensor_id: str) -> List[Document]:
        try:
            query = {
                "sensor_id": {"$gte": sensor_id}
            }
            results = self.collection.find(query)
            
            # Format data for LangChain
            documents = [
                Document(page_content=f"Temperature: {doc['temperature']}, Humidity: {doc['humidity']}, AQI: {doc['AQI']}, CO2_level: {doc['CO2_level']}", metadata={"timestamp": doc["timestamp"], "sensor": doc["sensor_id"]})
                for doc in results
            ]
            return documents
        except Exception as e:
            return {str(e)}


def get_sensor_data(sensor_id=None, for_rag=False):
    """Retrieve sensor data from MongoDB."""
    try:
        retriever = MongoDBRetriever(MONGO_URI, DB_NAME, COLLECTION_NAME)
        if sensor_id:
            print("Retrieving by id")
            documents = retriever.retrieve_data_by_id(sensor_id=sensor_id)
        elif for_rag:
            print("Retrieving yesterday data")
            yesterday = datetime.now() - timedelta(days=1)
            yesterday_start = datetime(yesterday.year, yesterday.month, yesterday.day)  # Midnight at the start of yesterday
            yesterday_end = yesterday_start + timedelta(days=1)  # Midnight at the start of today
            documents = retriever.retrieve_data(start_date=yesterday_start, end_date=yesterday_end)
        else:
            print("Retrieving all")
            one_week_ago = datetime.now(timezone.utc) - timedelta(weeks=1)
            documents = retriever.retrieve_data(start_date=one_week_ago, end_date=datetime.now(timezone.utc))
        doc_list = list(documents)
        print(doc_list)

        return doc_list
    except Exception as e:
        return {str(e)}

def update_knowledge_base():
    try:
        retriever = MongoDBRetriever(MONGO_URI, DB_NAME, COLLECTION_NAME)
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_start = datetime(yesterday.year, yesterday.month, yesterday.day)  # Midnight at the start of yesterday
        yesterday_end = yesterday_start + timedelta(days=1)  # Midnight at the start of today
        data = retriever.retrieve_data_for_kb(start_date=yesterday_start, end_date=yesterday_end)

        # Open a text file to write the data
        with open("sensor_data.txt", "w") as file:
            for record in data:
                # Format the record to a readable format
                record_str = (
                    f"Sensor ID: {record['sensor_id']}\n"
                    f"Timestamp: {record['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Temperature: {record['temperature']} °C\n"
                    f"Humidity: {record['humidity']} %\n"
                    f"AQI: {record['AQI']}\n"
                    f"CO2 Level: {record['CO2_level']} ppm\n"
                    f"ID: {record['id']}\n\n"
                )
                
                # Write the formatted record to the text file
                file.write(record_str)

        print("Data written to sensor_data.txt")

        # Load the TXT
        loader = TextLoader("sensor_data.txt", encoding = 'UTF-8')
        data = loader.load()

        # Split the data into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=20)
        documents = text_splitter.split_documents(data)

        # Prepare documents for insertion
        docs_to_insert = [{
            "text": doc.page_content,
            "embedding": generate_embedding(doc.page_content)
        } for doc in documents]

        # Connect to your Atlas cluster
        ca = certifi.where()
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client[VECTOR_DB_NAME]
        vector_collection = db[VECTOR_COLLECTION_NAME]

        # Insert documents into the collection
        result = vector_collection.insert_many(docs_to_insert)
        
        print(result)
    except Exception as e:
        return {str(e)}

# update_knowledge_base()


