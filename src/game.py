from pymongo import MongoClient
from random import randrange

# mongodb credential
cred="admin:password123"

client = MongoClient(f"mongodb://{cred}@localhost:27017")
db = client.pokemon

pc_collection = db.pc
pokedex_collection = db.pokedex

# returns the entire pokedex collection as a list
def get_pokedex():
    pokedex_data = list(pokedex_collection.find({}))
    return pokedex_data

# returns the entire pc collection as a list
def get_pc():
    pc_data = list(pc_collection.find({}))
    return pc_data

def get_pokemon_from_name(name):
    result = list(pc_collection.find({"name":name}))
    if len(result) == 1:
        return result[0]
    else:
        return None

def battle(name):
    result = list(pc_collection.find({"name":name}))
    my_pokemon = None
    if len(result) == 1:
        my_pokemon = result[0]
    else:
        return { "msg":"Error Occurred!" }

    available_pokemon = pc_collection.count_documents({})

    random_pokemon = my_pokemon
    # ensure random pokemon we are going to fight
    # is not the pokemon we are using
    while random_pokemon == my_pokemon:
        random_index = randrange(0, available_pokemon)
        random_pokemon = list(pc_collection.find({}))[random_index]
        
    if "xp" in random_pokemon and "hp" in random_pokemon:
        return { "enemy":random_pokemon["name"] }
    else:
        return { "msg":"Error Occurred!" }

def battle_resolve(choice:str, red_pokemon, blue_pokemon):
    if choice.lower() == "fight":
        hp_decrease = -randrange(0, 5)
        xp_increase = randrange(5, 10)

        # your pokemon lost health and gained XP
        pc_collection.update_one(
            { "_id": red_pokemon["_id"] },
            {"$inc": {"hp": hp_decrease}}
        )
        pc_collection.update_one(
            { "_id": red_pokemon["_id"] },
            {"$inc": {"xp": xp_increase}}
        )

        return { "msg":"You Won!" }
    else:
        # opponent gains XP
        pc_collection.update_one(
            {"_id": blue_pokemon["_id"]},
            {"$inc": {"xp": randrange(5, 10)}}
        )
        
        return { "msg":"You Fled!" }