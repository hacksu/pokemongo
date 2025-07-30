from pymongo import MongoClient
from random import randrange

client = MongoClient("mongodb://localhost:27017")
db = client.pokemon

pc_collection = db.pc
pokedex_collection = db.pokedex

# returns the entire pokedex collection as a list
def get_pokedex():
    pokedex_data = list(pokedex_collection.find({}))
    return pokedex_data

# returns the pc collection as a list
def get_pc():
    pc_data = list(pc_collection.find({}))
    return pc_data
