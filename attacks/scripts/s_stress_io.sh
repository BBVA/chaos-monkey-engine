#!/bin/bash
set -m

sudo docker run -d lorel/docker-stress-ng --hdd 300 --io 300
