# Reverse geo-coding API 

Debian GNU/Linux 12

Python 3.11.2

FastAPI

## Set up instruction

#### Prepare OS, install git & python

- `sudo apt-get update && sudo apt-get upgrade`
- `sudo apt-get install git`
- `sudo apt-get install python3 && sudo apt-get install python3-pip && sudo apt-get install python3-venv`

#### Clone repo
- `git clone https://github.com/dratdin/revgeocode_api.git`
- `cd revgeocode_api`

#### Create & activate python venv
- `python3 -m venv py_venv`
- `. ./py_venv/bin/activate`

#### Install pip requirements
- `pip install -r requirements.txt`

#### Run application
- `fastapi dev main.py`
