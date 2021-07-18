#!/bin/bash

docker stop slowtcp_instance
docker rm slowtcp_instance
docker rmi slowtcp

docker build -t slowtcp .
