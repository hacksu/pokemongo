from pymongo import MongoClient

# mongodb credential
cred="admin:password123"
client = MongoClient(f"mongodb://{cred}@localhost:27017")

db = client.pokemon
collection = db.pc

# each insert will create a new object entry with a new ObjectId
# if duplicate protection is needed you need to add extra checks
insertResult = collection.insert_one({
  "name": "Delozier",
  "species": "Wartortle",
  "hp": 100,   # important
  "xp": 0,     # important
  "mood": "bemused"
})
print(insertResult.inserted_id)
print(insertResult)

# show insertion is present
findResult = list(collection.find({
  "name": "Delozier"
}))
print(findResult)