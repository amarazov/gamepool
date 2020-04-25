#!/usr/bin/env bash

rm -rf app.db migrations/

flask db init
flask db migrate
flask db upgrade

flask appcfg games app/games/init_games.csv
flask appcfg sessions app/games/init_sessions.csv
