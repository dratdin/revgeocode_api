# Reverse geo-coding API 

Tested on
Debian GNU/Linux 12
MacOS 14.4.1 

Python 3.11.2

FastAPI

## Set up instruction

#### Prepare OS, install git & python (Debian only)

- `sudo apt-get update && sudo apt-get upgrade`
- `sudo apt-get install git`
- `sudo apt-get install python3 && sudo apt-get install python3-pip && sudo apt-get install python3-venv`

#### Clone repo
- `git clone https://github.com/dratdin/revgeocode_api.git`
- `cd revgeocode_api`

#### Create & activate python venv
- `python3 -m venv venv`
- `. ./venv/bin/activate`

### Upgrade pip
- `pip install --upgrade pip`

#### Install pip requirements
- `pip install -r requirements.txt`

#### Run application
- `fastapi dev main.py`
