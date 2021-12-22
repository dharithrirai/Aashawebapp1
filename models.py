from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app = Flask(__name__)
db = SQLAlchemy()

#login/sign-up
class User(db.Model):
      __tablename__ = 'Users'
      id = db.Column(db.Integer, primary_key=True)
      Hid = db.Column(db.String(40), unique=True, nullable=False)
      Hname = db.Column(db.String(40), unique=True, nullable=False)
      Hemail = db.Column(db.String(40), unique=True, nullable=False)
      Password = db.Column(db.String(40))

def __init__(self, Hid, Hname, Hemail, Password):
    self.Hid = Hid
    self.Hname = Hname
    self.Hemail =Hemail
    self.Password = Password

#patient intake form
class Formm(db.Model):
    __tablename__ = 'formm'
    id = db.Column(db.Integer, primary_key=True)
    Hid=db.Column(db.String(40), nullable=False)
    Pname = db.Column(db.String(40), nullable=False)
    Pemail = db.Column(db.String(40), unique=True)
    Dob = db.Column(db.String(40),  nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Height = db.Column(db.String(40), nullable=False)
    Weight = db.Column(db.String(40), nullable=False)
    Bp= db.Column(db.String(40), nullable=False)
    Sugar= db.Column(db.String(40), nullable=False)
    Mdate= db.Column(db.String(40), nullable=False)
    Pexp= db.Column(db.String(4000), nullable=False)
    Protocol= db.Column(db.String(4000), nullable=False)


def __init__(self, Hid, Pname, Pemail, Dob, Age, Height, Weight, Bp, Sugar, Mdate, Pexp, Protocol):
    self.Hid = Hid
    self.Pname = Pname
    self.Pemail = Pemail
    self.Dob = Dob
    self.Age = Age
    self.Height = Height
    self.Weight =Weight
    self.Bp = Bp
    self.Sugar = Sugar
    self.Mdate = Mdate
    self.Pexp = Pexp
    self. Protocol=Protocol

#image-process
class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    Hid = db.Column(db.String(400), nullable=False)
    Pname = db.Column(db.String(400), nullable=False)
    name=db.Column(db.String(400))
    file=db.Column(db.LargeBinary)

def __init__(self, Hid, Pname, file):
    self.Hid = Hid
    self.Pname = Pname
    self.file=file
#appointment
class Appoint(db.Model):
    __tablename__ = 'appoint'
    id = db.Column(db.Integer, primary_key=True)
    Hid = db.Column(db.String(40),  nullable=False)
    Pname = db.Column(db.String(40),  nullable=False)
    Pcontact = db.Column(db.String(40),  nullable=False)
    Pdate = db.Column(db.String(40),  nullable=False)
    Ptime = db.Column(db.String(40),  nullable=False)

    def __init__(self, Hid, Pname,Pcontact, Pdate, Ptime):
        self.Hid = Hid
        self.Pname = Pname
        self.Pcontact = Pcontact
        self.Pdate = Pdate
        self.Ptime = Ptime


