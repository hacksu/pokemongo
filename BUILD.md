# PokeMongo
## :hammer: Build
```bash
# Install dependency packages
sudo apt update && sudo apt install python3 \
python3-pip \
python3-venv \
docker.io

# move into cloned repo dir
cd pokemongo

# Build the custom mongodb docker image
docker build --build-arg PASSWORD=password123 -t pokemongo .
# Run the image locally
docker run -d --name pokemongo_db -p 27017:27017 pokemongo

# Build VENV for flask app interface
python3 -m venv venv
source venv/bin/activate
# install python packages
pip install pymongo flask

# run flask server
python3 src/app.py
```