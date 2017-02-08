#!/bin/bash
set -m

sudo docker run -d lorel/docker-stress-ng --cpu 300
