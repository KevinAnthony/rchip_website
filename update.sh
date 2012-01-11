#!/bin/bash
git update
./migrate.sh
./clean.sh
service apache2 restart
