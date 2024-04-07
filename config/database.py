from pymongo import MongoClient

client = MongoClient("mongodb+srv://anujapurohit19:5ZtZz22k9l3CRONW@cluster0.ltqewat.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.Library_db

collection_name = db["Library_collection"]