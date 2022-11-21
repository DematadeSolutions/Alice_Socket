#!/bin/bash

CONTAINER_NAME="alice-socket"
IMAGE_NAME="alice-socket"
SRC=~/Alice_Socket
set +x
echo "=================="
echo "|Pulling the code|"
echo "=================="
echo ""
cd $SRC && git pull
echo ""

echo "======================="
echo "|Building the codebase|"
echo "======================="
echo ""
docker build -t $IMAGE_NAME .
echo ""
echo "==========================="
echo "|DEPLOYING THE APPLICATION|"
echo "==========================="
echo ""


docker rm -f $CONTAINER_NAME

docker run -d -p 8003:8003 --restart always --name $CONTAINER_NAME $IMAGE_NAME


echo ""
echo "==============================================="
echo "| $IMAGE_NAME APPLICATION DEPLOYMENT COMPLETED|"
echo "==============================================="
echo ""
