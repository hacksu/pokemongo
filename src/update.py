from pprint import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId

# mongodb credential
cred="admin:password123"
client = MongoClient(f"mongodb://{cred}@localhost:27017")

db = client.pokemon
collection = db.pc

name = "Esther"
name_query = { "name": name }

print("updating owner...")
collection.update_one(
    name_query,
    {"$set": {"owner": "Mitch"}}
)
pprint(collection.find_one(name_query))

print("\nincrementing health...")
collection.update_one(
  name_query,
  { "$inc": {"hp": 5} }
)
pprint(collection.find_one(name_query))
