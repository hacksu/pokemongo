#!/bin/bash

# Local variable
$DB_NAME=pokemon

cd /app

# Enter venv session
source ./bin/activate

# Install python dependencies
cd src
pip install -r requirements.txt

# Start MongoDB in the background if it's not already running
mongod --bind_ip 0.0.0.0 --fork --logpath /var/log/mongod.log

# Wait for MongoDB to be ready (adjust the sleep time if needed)
sleep 10

# Connect to mongodb and set up an initial state
mongosh <<EOF
use $DB_NAME

db.createUser({
    user: "admin",
    pwd: "$PASSWORD",
    roles: [{ role: "readWrite", db: "$DB_NAME" }]
})
EOF

# Create the pokedex collection from existing JSON file
mongoimport --db $DB_NAME --collection pokedex --file /app/data/pokedex.json --jsonArray

# Create the PC collection from existing JSON file
mongoimport --db $DB_NAME --collection pc --file /app/data/extra_pc_pokemon.json --jsonArray

# Start Flask App
python3 app.py

# Keep container alive
# (WITH OUT THIS THE CONTAINER WILL CLOSE INSTANTLY)
tail -f /dev/null
