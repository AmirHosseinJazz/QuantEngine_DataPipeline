#!/bin/bash

# ANSI Color Codes
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# ANSI Escape Codes for bold and reset
BOLD='\033[1m'
RESET='\033[0m'

if [ ! -d "docker_volume" ]; then
  mkdir "docker_volume"
  echo -e "   ${GREEN}Folder created:${BOLD}docker_volume${NC}"
  chmod 755 "docker_volume"
  echo -e "   ${GREEN}Permissions set to 755 for folder:${BOLD}docker_volume${NC}"
else
  echo -e "   ${GREEN}Folder already exists:${BOLD}docker_volume${NC}"
fi


if [ ! -d "docker_init" ]; then
  mkdir "docker_init"
  echo -e "   ${GREEN}Folder created:${BOLD}docker_init${NC}"
  sudo chmod 755 "docker_init"
  echo -e "   ${GREEN}Permissions set to 755 for folder:${BOLD}docker_init${NC}"
  ## if .sh file in the folder chmod +x
  if [ -f "docker_init/init.sh" ]; then
    sudo chmod +x "docker_init/init.sh"
    echo -e "   ${GREEN}Permissions set to 755 for file:${BOLD}docker_init/init.sh${NC}"
  fi
else
  echo -e "   ${GREEN}Folder already exists:${BOLD}docker_init${NC}"
fi



# Define the directories where Volume folders are located

folder_names=("postgres_data" "redis_data" "timescaledb_data")

for folder_name in "${folder_names[@]}"; do
    # Check if the folder does not exist
    if [ ! -d "docker_volume/$folder_name" ]; then
        # Create the folder
        mkdir "docker_volume/$folder_name"
        echo -e "${GREEN}   Folder created: docker_volume/$folder_name${NC}"
    else
        echo -e "${GREEN}   Folder already exists: docker_volume/$folder_name${NC}"

    fi

    sudo chmod 755 "docker_volume/$folder_name"
    echo -e "${GREEN}  Permissions set to 755 for folder:$folder_name${NC}"
done


# Define the directories where Dockerfiles are located
directories=("perfect_server" "forex_historic" "crypto_historic" "crypto_live")
for dir in "${directories[@]}"; do
  if [ -d "./$dir/.env" ]; then
    rm -r "./$dir/.env"
  fi
  cp .env ./$dir/
  
  if [ -f "./$dir/entrypoint.sh" ]; then
    chmod +x ./$dir/entrypoint.sh
  fi
done


