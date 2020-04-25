#!/bin/sh
source venv/bin/activate

while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done

flask translate compile

flask appcfg games app/games/init_games.csv
flask appcfg sessions app/games/init_sessions.csv

exec gunicorn -b :5000 --access-logfile - --error-logfile - gamepool:application
