# argument that creates a env variable the docker uses
# example: docker build --build-arg PASSWORD=supersecurepassword123 -t image_name .
FROM mongo:latest

ARG PASSWORD

# mongo env vars
ENV MONGO_INITDB_ROOT_USERNAME=admin
ENV MONGO_INITDB_ROOT_PASSWORD=${PASSWORD}

# set up app file structure
WORKDIR /

EXPOSE 27017

COPY pokemon_data /data

# prep bash init script
COPY init.sh /root/init.sh
# bash files you want to execute need to be set as executable
RUN chmod +x /root/init.sh

# Commands that will be executed after the build process
CMD [ "/bin/bash", "/root/init.sh" ]