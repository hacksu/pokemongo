from pprint import pprint  # not a mongodb thing, but useful for displaying documents
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.pokemon
collection = db.pokedex

pikachu = collection.find_one({"name": "Pikachu"})
pprint(pikachu)
print("Pikachu's base HP:", pikachu["HP"])

good_hp = collection.find_one({ "HP": {"$gt": 120} })
pprint(good_hp)

bad_hp_list = list(collection.find({"HP": {"$lt": 15}}))
pprint(bad_hp_list)

multiple_queries = [
    { "HP": {"$gt": 120}},
    {"Defence": {"$gt": 210}}
]
good_hp_or_good_defence = list(collection.find({ "$or": multiple_queries }))
pprint(good_hp_or_good_defence)

pprint(collection.find_one({"type": "Flying"}))

pprint(collection.find_one({"Special.Attack": 109}))
