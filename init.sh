#!/bin/bash

# safely bash flag
set -e

# Local variable
DB_NAME=pokemon

# Start MongoDB without auth
mongod --bind_ip 0.0.0.0 --fork --logpath /var/log/mongod.log

# Function to check if a collection is empty
is_collection_empty() {
  local collection=$1
  local count=$(mongosh --quiet --eval "db.getSiblingDB('$DB_NAME').$collection.countDocuments({})")
  [[ "$count" -eq 0 ]]
}

# Import pokedex if empty
if is_collection_empty "pokedex"; then
  echo "Importing pokedex.json..."
  mongoimport --db $DB_NAME --collection pokedex --file /data/pokedex.json --jsonArray
else
  echo "Skipping pokedex import — collection already populated."
fi

# Import PC if empty
if is_collection_empty "pc"; then
  echo "Importing extra_pc_pokemon.json..."
  mongoimport --db $DB_NAME --collection pc --file /data/extra_pc_pokemon.json --jsonArray
else
  echo "Skipping PC import — collection already populated."
fi

# Setup authentication
mongosh <<EOF
use admin
db.createUser({
    user: "$MONGO_INITDB_ROOT_USERNAME",
    pwd: "$MONGO_INITDB_ROOT_PASSWORD",
    roles: [{ role: "root", db: "admin" }]
})
EOF

# Setup data for nosql showcase
mongosh <<EOF
use trainers
db.trainers.insertMany([
  {
    username: "ash",
    password: "pikachu123"
  },
  {
    username: "misty",
    password: "waterqueen"
  },
  {
    username: "brock",
    password: "onixrocks"
  }
])
EOF

# Restart mongod with auth enabled
mongod --shutdown
mongod --bind_ip 0.0.0.0 --auth --fork --logpath /var/log/mongod.log

# Keep container alive
tail -f /dev/null