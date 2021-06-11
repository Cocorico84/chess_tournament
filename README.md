# Description

The chess manager provides a menu to handle a tournament of chess. 

List of possible actions:

- Create a tournament
- Add players in the tournament
- Write match results
- Change the rank of a player
- Get a report

You can launch a tournament only if there are 8 recorded players in the tournament.
Saving is automatic. Each action is saved in the database.

# Prerequisites

Python 3

# Installation

On Linux or Mac
```console
pip install virtualenv
virtualenv venv --python=python3
source venv/bin/activate
pip install -r requirements.txt
```

On Windows
```console
c:\Python38\python -m venv c:\path\to\myenv
C:\\{venv}\\Scripts\\activate.bat
pip install -r requirements.txt
```

# Quickstart

```console
python main.py
```
When you launch this command, it will create you a database called "db.json". If you want more information about TinyDB you can go in their [website](https://tinydb.readthedocs.io/en/stable/index.html#)

# Code Style
```
flake8 .
```
To get a report. It will create a directory named "flake8-report". Then you can open index.html in a browser.
```
flake8 --format=html --htmldir=flake8-report
```
# Contributor

If you have any suggestions to improve the chess manager, you can create an issue.