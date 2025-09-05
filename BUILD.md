# PokeMongo
## :hammer: Build
```bash
# clone the repo
git clone https://github.com/hacksu/pokemongo.git

# Install system dependency packages
sudo apt update && sudo apt install python3 \
python3-pip \
python3-venv \
docker.io

# move into cloned repo dir
cd pokemongo

# Build the custom mongodb docker image
sudo docker build --build-arg PASSWORD=password123 -t pokemongo .
# Run the image locally
sudo docker run -d --name pokemongo_db -p 27017:27017 pokemongo

# Build VENV for flask app interface to interact with the mongodb docker
python3 -m venv venv
source venv/bin/activate
# install python packages
pip install -r requirements.txt

# run flask server
python3 src/app.py
```

### :warning: Notice
Within the following python files: `game.py, insert.py, queries.py, update.py` ensure the credential string is properly updated based on the `PASSWORD=` build argument, ie: if you ran `PASSWORD=supersecretpassword!` you need to update each python files cred variable to `cred="admin:supersecretpassword!"` or else the python scripts will not be able to connect to your local mongoDB!