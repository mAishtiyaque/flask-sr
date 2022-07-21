from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String
#from sqlalchemy.orm import declarative_base
#Base = declarative_base()

#from config import DevelopmentConfig as config
from config import ProductionConfig as config
from flask_cors import CORS
app=Flask(__name__)
CORS(app, resources={r"/users/*": {"origins": "*"}})
app.config.from_object(config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    userid = Column(String,primary_key=True)
    passw = Column(String)
    fname = Column(String)
    lname = Column(String)

    def __init__(self,userid,passw,fname,lname):
        super().__init__()
        self.userid=userid
        self.passw=passw
        self.fname=fname
        self.lname=lname
    
    def serialize(self):
        return {'userid':self.userid,'passw':self.passw,'fname':self.fname,
                'lname':self.lname}

class Userdata(db.Model):
    __tablename__ = 'userdata'
    userid = Column(String,primary_key=True)
    textid = Column(String,primary_key=True)
    rtext = Column(String)

    def __init__(self,userid,textid,rtext):
        super().__init__()
        self.userid=userid
        self.textid=textid
        self.rtext=rtext
    
    def serialize(self):
        return [self.rtext,int(self.textid)]

class Tokens(db.Model):
    __tablename__ = 'tokens'
    userid = Column(String,primary_key=True)
    token = Column(String,primary_key=True)

    def __init__(self,userid,token):
        super().__init__()
        self.userid=userid
        self.token=token
    def __repr__(self):
        return '<Token {}>'.format(self.userid)
    
    def serialize(self):
        return {'userid':self.userid,'token':self.token}