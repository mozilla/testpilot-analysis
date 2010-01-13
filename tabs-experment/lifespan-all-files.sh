#!/bin/bash

for file in /var/www/testpilot/storage/1-csv/*
do
    python tab-avg-lifespan.py ${file}
done
