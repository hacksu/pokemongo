from pprint import pprint  # not a mongodb thing, but useful for displaying documents
from pymongo import MongoClient

# mongodb credential
cred="admin:password123"
client = MongoClient(f"mongodb://{cred}@localhost:27017")

db = client.pokemon
collection = db.pokedex

pikachu = collection.find_one({"name": "Pikachu"})
print("########### FIND PIKACHU ###########")
pprint(pikachu)
print("Pikachu's base HP:", pikachu["HP"])
print("####################################\n")


print("########### FIND GOOD HEALTH ###########")
good_hp = collection.find_one({ "HP": {"$gt": 120} })
pprint(good_hp)
print("########################################\n")


print("########### FIND LOW HEALTH ###########")
bad_hp_list = list(collection.find({"HP": {"$lt": 15}}))
pprint(bad_hp_list)
print("#######################################\n")


print("########### FIND HIGH HEALTH & DEFENCE ###########")
multiple_queries = [
    { "HP": {"$gt": 120}},
    {"Defence": {"$gt": 210}}
]

good_hp_or_good_defence = list(collection.find({ "$or": multiple_queries }))
pprint(good_hp_or_good_defence)
print("##################################################\n")

print("########### FIND FLYING TYPE ###########")
pprint(collection.find_one({"type": "Flying"}))
print("########################################\n")


print("########### FIND SPECIAL ATTACK ###########")
pprint(collection.find_one({"Special.Attack": 109}))
print("###########################################\n")