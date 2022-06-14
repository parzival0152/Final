import json
from typing import Iterator, Tuple
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from Models.functions import complition_email_send, fail_email_send, create_stats

db = SQLAlchemy()

default_preferances = json.dumps({
    "alert_time":"12:00"
})

past_documents_table = db.Table(
    "past_documents",
    db.Column("user", db.ForeignKey("users.id")),
    db.Column("document", db.ForeignKey("documents.Did"))
)

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    fullname = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    preferances = db.Column(db.JSON, nullable=False)

    created_templates = db.relationship("Template", backref="owner")
    
    created_documents = db.relationship("Document", backref="owner", foreign_keys="[Document.owner_id]")
    pending_documents = db.relationship("Document", foreign_keys="[Document.currentemail]")
    past_documents = db.relationship("Document", secondary=past_documents_table)


    def __init__(self,username,fullname,email,password) -> None:
        self.username = username
        self.fullname = fullname
        self.email = email
        self.password = password
        self.preferances = default_preferances

    def __repr__(self) -> str:
        return f"<User {self.id}>"

    def get_info(self):
        return {
            "id":self.id,
            "name":self.fullname,
            "email":self.email,
            "preferances":json.loads(self.preferances)
        }

    def toJSON(self):
        return {
            "id":self.id,
            "username":self.username,
            "fullname":self.fullname,
            "email":self.email,
            "password":self.password,
            "preferances":json.loads(self.preferances),
            "my templates":[t.__repr__() for t in self.created_templates],
            "my documents":[d.__repr__() for d in self.created_documents],
            "pending documents":[d.__repr__() for d in self.pending_documents],
            "past documents":[d.__repr__() for d in self.past_documents]
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

    def __init__(self,owner:User,form_response) -> None:
        self.name = form_response["title"]
        self.description = form_response["description"]
        self.data = json.dumps(form_response)
        self.stats = create_stats(form_response)
        self.owner_id = owner.id
    
    def __repr__(self) -> str:
        return f"<Template {self.Tid}>"

    def get_info(self):
        return {
            "name":self.name,
            "description":self.description,
            "creator":self.owner.fullname,
            "Tid":self.Tid,
            "href":f"/templates/{self.Tid}"
        }
    
    def toJSON(self):
        return {
            "Tid":self.Tid,
            "name":self.name,
            "description":self.description,
            "data":json.loads(self.data),
            "stats":json.loads(self.stats),
            "owner":self.owner.__repr__()
        }

    def instanciate(self,current_user):
        stats = json.loads(self.stats)
        stats["created"] += 1
        stats["Stage #0"] += 1
        self.stats = json.dumps(stats)
        data = json.loads(self.data)
        data["stations"][0]["Email"] = current_user.email
        return Document(
            data = json.dumps(data),
            owner_id = current_user.id,
            master_Tid = self.Tid,
            stage = 0,
            currentemail = current_user.email
        )
    

class Document(db.Model):
    __tablename__ = "documents"
    
    Did = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    master_Tid = db.Column(db.Integer, db.ForeignKey("templates.Tid"))
    stage = db.Column(db.Integer)
    currentemail = db.Column(db.String(255), db.ForeignKey("users.email"))

    master_template = db.relationship("Template")

    def __repr__(self) -> str:
        return f"<Document {self.Did}>"

    def get_info(self):
        return {
            "name":self.master_template.name,
            "description":self.master_template.description,
            "creator":self.owner.fullname,
            "Did":self.Did,
            "href":f"/documents/{self.Did}"
        }

    def toJSON(self):
        return {
            "name":self.master_template.name,
            "description":self.master_template.description,
            "creator":self.owner.fullname,
            "Did":self.Did,
            "data":json.loads(self.data),
            "stage":self.stage
        }
    
    def advance(self,response_data):
        data = json.loads(self.data)
        stage = self.stage
        choice = response_data['choice']

        data = response_data["data"]

        nextemail = ""
        completed = False
        try:
            nextemail = data["stations"][stage+1]["Email"]
        except IndexError:
            completed = True

        origintemplate = self.master_template
        stats = json.loads(origintemplate.stats)
        stats[f"Stage #{stage}"] -= 1
        
        if choice == "reject":
            stats["failed"]+=1
            nextemail = ""
            fail_email_send(self.owner)
        else:
            if completed:
                stats["completed"]+=1
                complition_email_send(self.owner)
            else:
                stats[f"Stage #{stage+1}"] += 1
            

        self.data = json.dumps(data)
        self.stage += 1
        self.currentemail = nextemail
        origintemplate.stats = json.dumps(stats)