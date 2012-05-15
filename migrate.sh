#!/bin/bash
apps=(weight mile rchip schedule)
for app in ${apps[@]}
  do
    ./manage.py schemamigration $app --auto
    ./manage.py migrate $app
  done
