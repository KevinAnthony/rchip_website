#!/bin/bash
apps=(main weight mile rchip schedule blog)
for app in ${apps[@]}
  do
    ./manage.py schemamigration $app --auto
    ./manage.py migrate $app
  done
