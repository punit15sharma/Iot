run "bash infana.sh"
Commands for creating a database and granting all the premissions

"""

create database home
use home

create user grafana with password '<passwordhere>' with all privileges
grant all privileges on home to grafana

show users

"""
#one has to add the database(grafana) on Grafana server too 
