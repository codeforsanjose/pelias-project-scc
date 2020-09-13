# pelias-project-scc
Project for the [Pelias geocoder](https://pelias.io/) for [addresses in the County of Santa Clara](https://data.sccgov.org/Government/AddressPoint/k4vk-5ggi)

## Setup
Mostly, download the County data and follow the "quickstart" directions for the [Docker setup](https://github.com/pelias/docker/). Like this:

```bash
#!/bin/bash

# clone the Pelias docker repository
git clone https://github.com/pelias/docker.git

# install pelias script
ln -s "$(pwd)/docker/pelias" ~/.local/bin/pelias

# clone this repository
git clone https://github.com/codeforsanjose/pelias-project-scc.git

# cd into the project directory
cd pelias-project-scc

# create a directory to store Pelias data files
mkdir ./data

# configure docker to write files as your local user
# see: https://github.com/pelias/docker#variable-docker_user
# note: use 'gsed' instead of 'sed' on a Mac
sed -i '/DOCKER_USER/d' .env
echo "DOCKER_USER=$(id -u)" >> .env

# download the address data
curl https://data.sccgov.org/api/views/qt6v-9zrp/rows.csv?accessType=DOWNLOAD --output AddressPoint_data.csv

# transform into a good format for Pelias
python clean_address_csv.py

# run build
pelias compose pull
pelias elastic start
pelias elastic wait
pelias elastic create
pelias download all
pelias prepare all
pelias import all
pelias compose up
```
