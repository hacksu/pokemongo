from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.pokemon
collection = db.pc

result = collection.insert_one({
  "name": "Squinchy",
  "species": "Wartortle",
  "hp": 100,   # important
  "xp": 0,     # important
  "mood": "bemused"
})
print(result.inserted_id)
