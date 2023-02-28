#!/bin/bash

# List of container IDs/names to save logs for
CONTAINERS=("shai_devops-app1-1" "shai_devops-app2-1" "shai_devops-app3-1" "shai_devops-mysql-1")

# Loop through each container and save its logs to a separate file
for CONTAINER in "${CONTAINERS[@]}"
do
    docker logs "$CONTAINER" > ../"${CONTAINER}_logs.txt"
done