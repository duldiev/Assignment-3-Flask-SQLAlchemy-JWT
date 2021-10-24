from datetime import datetime
from flaskblog import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    token = db.Column(db.Text, nullable=False, default='')

    def __init__(self, username, email, password, token):
        self.username = username
        self.email = email
        self.password = password
        self.token = token
