### Kyeongsoo's Toy Project
---

on powershell

```
Not much implemented
. .\activate.ps1
(venv) pip install sqlalchemy flask flask-sqlalchemy python-dotenv
venv/Scripts/python -m pip freeze > requirements.txt
venv/Scripts/python -m pip install -r requirements.txt

flask run # for run web server
flask shell # for run shell with app_context
```

in ipython

```
%lsmagic
%%file file.py
%%file -a file.py
%load file.py
%run file.py
```

.env 

```
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_RUN_PORT=5001
SQLALCHEMY_DATABASE_URI=sqlite+pysqlite:///:memory:
```
