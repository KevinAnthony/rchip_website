#!/bin/bash
apps=(weight mile rchip schedule)
for app in ${apps[@]}
  do
    python2.7 manage.py schemamigration $app --auto
    python2.7 manage.py migrate $app
  done
