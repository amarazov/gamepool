#!/usr/bin/env bash

if [ $# -ne 2 ];
    then echo "Usage: $0 old_game new_game"
    exit 1
fi

mkdir $2
cd $2/
mkdir templates
mkdir static
cp ../$1/__init__.py ../$2/__init__.py
sed -i -e "s/$1/$2/g" ../$2/__init__.py

cp ../$1/routes.py ../$2/routes.py
sed -i -e "s/$1/$2/g" ../$2/routes.py

cp ../$1/templates/$1_game.html templates/$2_game.html
sed -i -e "s/$1/$2/g" templates/$2_game.html
