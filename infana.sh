#!/bin/sh

sudo apt update
sudo apt upgrade -y

wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add - 
source /etc/os-release
echo "deb https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

sudo apt update && sudo apt install -y influxdb

sudo systemctl unmask influxdb.service
sudo systemctl start influxdb
sudo systemctl enable influxdb.service

wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

sudo apt update && sudo apt install -y grafana

sudo systemctl unmask grafana-server.service
sudo systemctl start grafana-server
sudo systemctl enable grafana-server.service


curl -L https://raw.githubusercontent.com/headmelted/codebuilds/master/docs/installers/apt.sh | sudo bash
