from pprint import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017")
db = client.pokemon
collection = db.PC

my_id = ObjectId("63868cffb0beba066ce5624c")
id_query = { "_id": my_id }

print("updating owner...")
collection.update_one(
    id_query,
    {"$set": {"owner": "Mitch"}}
)
pprint(collection.find_one(id_query))

print("incrementing health...")
collection.update_one(
  id_query,
  { "$inc": {"hp": 5} }
)
pprint(collection.find_one(id_query))
