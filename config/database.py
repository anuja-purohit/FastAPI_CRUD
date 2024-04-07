from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()

database_url=os.getenv("DATABASE_URL")
client = MongoClient(database_url)

db = client.Library_db

collection_name = db["Library_collection"]