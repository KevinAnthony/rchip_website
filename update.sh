#!/bin/bash

#update main program
git update

#cleanup
./migrate.sh
./clean.sh
service apache2 restart
