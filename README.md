# Gamepool

A pool of games which can track the cognitive abilities of the registered users through time.

## Configuration

```
export FLASK_APP=gamepool.py
```

### Game configurations

A csv file with the game configurations has to be provided. Default is ```app/games/init_games.csv```


## Installation

```
virtualenv -p python3 venv; source venv/bin/activate
pip install -r requirements.txt
flask db init

flask db upgrade
flask initapp games app/games/init_games.csv
```

## Internationalization

```
flask translate init <language-code>
flask translate update
flask translate compile
```