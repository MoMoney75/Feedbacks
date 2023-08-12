from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete, update, ForeignKey
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename = 'users'

    username = db.Column(db.Text, primary_key=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    first_name = db.Column(db.Text, nullable=False, unique=False)
    last_name = db.Column(db.Text, nullable=False, unique=False)
    feedback = db.relationship('Feedback', backref="user", cascade="all,delete")


    @classmethod
    def register_user(cls,username,password,email,first_name,last_name):

        hashed_password = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed_password.decode("utf8")

        user = cls(username=username, password=hashed_utf8, email=email, first_name=first_name,last_name=last_name)
        db.session.add(user)


        return user

    @classmethod
    def authenticate_user(cls, username,pwd):
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
    
        else: 
            return False
        

class Feedback(db.Model):
    __tablename = 'feedback'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.Text,nullable=False)
    content = db.Column(db.Text,nullable=False)
    username = db.Column(db.Text,db.ForeignKey('user.username'),nullable=False,)


