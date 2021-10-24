# Authentication web server
## Installation
If you have pip on your system, you can simply install following packages:
* Flask
* Flask_WTF
* Flask_SQLAlchemy
* PyJWT

## Usage
* Import libraries
* Generate and set SECRET_KEY
* Set SQLALCHEMY_DATABASE_URI as postgreSQL or sqlite
```
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:port/database_name'
```

There's Users table in models.py. Create this table executing following code:
```
>>> from flaskblog import db
>>> from flaskblog.models import Users
>>> db.create_all()
```

After running the server, you can register new users from register page (all registered automatically stored in database). 

Then you can login with registered users. 

For every logged in users given new token. 

You can check token validity using this url and putting the token after **token=**

e.g. http://127.0.01:5000/protected?token=24230ifdsjfjdsklfj43943ut943
