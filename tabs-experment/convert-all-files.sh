#!/bin/bash

for file in /var/www/testpilot/storage/1/*
do
    python json-to-csv.py ${file} /var/www/testpilot/storage/1-csv/
    if [ $? -eq 0 ]
    then
        mv ${file} /var/www/testpilot/storage/1-json/
    fi
done

