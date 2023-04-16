import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
client.drop_database("bookstore")
assert "bookstore" not in client.list_database_names()
