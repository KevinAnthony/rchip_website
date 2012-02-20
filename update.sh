#!/bin/bash

#update dependancies
pip install --upgrade -e git://github.com/Fantomas42/django-blog-zinnia.git#egg=django-blog-zinnia
pip install --upgrade south
rm -rf src
rm -rf build

#update main program
git update

#cleanup
./migrate.sh
./clean.sh
service apache2 restart
