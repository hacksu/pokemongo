#!/bin/bash

# safely bash flag
set -e

# Local variable
DB_NAME=pokemon

mongod --bind_ip 0.0.0.0 --fork --logpath /var/log/mongod.log

# Create the pokedex collection from existing JSON file
mongoimport --db $DB_NAME --collection pokedex --file /data/pokedex.json --jsonArray

# Create the PC collection from existing JSON file
mongoimport --db $DB_NAME --collection pc --file /data/extra_pc_pokemon.json --jsonArray

# Setup authentication
mongosh <<EOF
use admin
db.createUser({
    user: "$MONGO_INITDB_ROOT_USERNAME",
    pwd: "$MONGO_INITDB_ROOT_PASSWORD",
    roles: [{ role: "root", db: "admin" }]
})
EOF

# Stop mongod to restart with auth for security
mongod --shutdown
mongod --bind_ip 0.0.0.0 --auth --fork --logpath /var/log/mongod.log

# Keep container alive
# (WITH OUT THIS THE CONTAINER WILL CLOSE INSTANTLY)
tail -f /dev/null