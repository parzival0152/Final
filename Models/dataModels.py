import json
from typing import Iterator, Tuple

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

from Models.functions import parse_response

db = SQLAlchemy()

default_preferances = json.dumps({
    "alert_time":"12:00"
})

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    fullname = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    preferances = db.Column(db.JSON, nullable=False)

    created_templates = db.relationship("Template")
    created_documents = db.relationship("Document")

    def __init__(self,username,fullname,email,password) -> None:
        self.username = username
        self.fullname = fullname
        self.email = email
        self.password = password
        self.preferances = default_preferances

    def toJSON(self):
        return {
            "id":self.id,
            "name":self.fullname,
            "email":self.email,
            "preferances":json.loads(self.preferances)
        }

    def update_preferances(self,items:Iterator[Tuple[str, str]]):
        pref = json.loads(self.preferances)
        for key,value in items:
            pref[key] = value
        self.preferances = json.dumps(pref)


class Template(db.Model):
    __tablename__ = "templates"

    Tid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    data = db.Column(db.JSON, nullable=False)
    stats = db.Column(db.JSON, nullable=False)

    owner = db.relationship("User")

    def __init__(self,owner:User,form_response) -> None:
        self.name = form_response["title"]
        self.description = form_response["description"]
        self.data, self.stats = parse_response(form_response)
        self.owner_id = owner.id

    def toJSON(self):
        return {
            "name":self.name,
            "description":self.description,
            "Tid":self.Tid
        }
    

class Document(db.Model):
    __tablename__ = "documents"
    
    Did = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    master_Tid = db.Column(db.Integer, db.ForeignKey("templates.Tid"))
    stage = db.Column(db.Integer)
    currentemail = db.Column(db.String(255))

    master_template = db.relationship("Template")
    owner = db.relationship("User")

    def toJSON(self):
        return {
            "name":self.master_template.name,
            "description":self.master_template.description,
            "creator":self.owner.fullname,
            "Did":self.Did
        }
