from fanclub.extensions import db

class User(db.Model):
    id = db.Column(db.String(100), unique=True, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    level = db.Column(db.Integer, default=1, nullable=False) 

