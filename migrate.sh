#!/bin/bash
apps=(main weight mile rchip)
for app in ${apps[@]}
  do
    ./manage.py schemamigration $app --auto
    ./manage.py migrate $app
  done
