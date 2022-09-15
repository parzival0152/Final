import json
from typing import Iterator, Tuple
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from Models.functions import complition_email_send, fail_email_send, create_stats

db = SQLAlchemy()

default_preferances = json.dumps({
    "alert_time":"12:00"
}) # default preferances are built here, this can be expended later with other preferances

past_documents_table = db.Table(
    "past_documents",
    db.Column("user", db.ForeignKey("users.id")),
    db.Column("document", db.ForeignKey("documents.Did"))
) # creating the secondary relational table that will hold the many to many relatioship of users and the documents that they have seen before

class User(db.Model, UserMixin):
    # User class for the ORM to interface with the sqlite database
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    fullname = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    preferances = db.Column(db.JSON, nullable=False)
    # these are all the data fields that are specific for a user

    created_templates = db.relationship("Template", backref="owner")
    # declaring a property of the class that acts as a relationship between it and the Template class
    
    created_documents = db.relationship("Document", backref="owner", foreign_keys="[Document.owner_id]")
    pending_documents = db.relationship("Document", foreign_keys="[Document.currentemail]")
    past_documents = db.relationship("Document", secondary=past_documents_table)
    # between the User and Document class there are 3 types of relationship that they can have
    # the first 2 being a one to many relationship with different keys
    # the last one, being a many to many relationship needs to use the secondary table that we have created earlier to establish itself


    def __init__(self,username,fullname,email,password):
        self.username = username
        self.fullname = fullname
        self.email = email
        self.password = password
        self.preferances = default_preferances
        # the initiation function to create a user entry

    def __repr__(self):
        return f"<User {self.id}>"
        #returning a simplified representation of the user

    def get_info(self):
        return {
            "id":self.id,
            "name":self.fullname,
            "email":self.email,
            "preferances":json.loads(self.preferances)
        }
        # return the user personal info

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
        # return a JSON representation of the user

    def update_preferances(self,items:Iterator[Tuple[str, str]]):
        pref = json.loads(self.preferances)
        for key,value in items:
            pref[key] = value
        self.preferances = json.dumps(pref)

        # input: iterator of string touples that represent the new preferances of the user
        # output: None
        # function: itirate and update any and all preferances that were given



class Template(db.Model):
    # Template class for the ORM to interface with the sqlite database
    __tablename__ = "templates"

    Tid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    data = db.Column(db.JSON, nullable=False)
    stats = db.Column(db.JSON, nullable=False)
    # relevant fields for Templates

    def __init__(self,owner:User,form_response):
        self.name = form_response["title"]
        self.description = form_response["description"]
        self.data = json.dumps(form_response)
        self.stats = create_stats(form_response)
        self.owner_id = owner.id
        # initiation function
    
    def __repr__(self):
        return f"<Template {self.Tid}>"
        # simplified string representation of the template

    def get_info(self):
        return {
            "name":self.name,
            "description":self.description,
            "creator":self.owner.fullname,
            "Tid":self.Tid,
            "href":f"/templates/{self.Tid}"
        }
        # return basic info about the template
        # the href property is the URI of the template from the POV of the client-side
    
    def toJSON(self):
        return {
            "Tid":self.Tid,
            "name":self.name,
            "description":self.description,
            "data":json.loads(self.data),
            "stats":json.loads(self.stats),
            "owner":self.owner.__repr__()
        }
        # return a JSON object of the entire content of the template

    def instanciate(self,current_user):
        # This function is called when a user wants to create a new document from this template
        
        stats = json.loads(self.stats)
        stats["created"] += 1
        stats["Stage #0"] += 1
        self.stats = json.dumps(stats)
        # load the statistics of the template and update them to add to the created count and to the first stage count

        data = json.loads(self.data)
        data["stations"][0]["Email"] = current_user.email
        # the email for the first station in a document is always that of the user that instanciated it
        # thus, before passing this data to the document we need to add the users email to the data of the template

        return Document(
            data = json.dumps(data),
            owner_id = current_user.id,
            master_Tid = self.Tid,
            stage = 0,
            currentemail = current_user.email
        )
        # we then create and return a new Document with the relevant data of the Template
        
    

class Document(db.Model):
    # Document class for the ORM to interface with the sqlite database
    __tablename__ = "documents"
    
    Did = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    master_Tid = db.Column(db.Integer, db.ForeignKey("templates.Tid"))
    stage = db.Column(db.Integer)
    currentemail = db.Column(db.String(255), db.ForeignKey("users.email"))
    # relevant fields for a document

    master_template = db.relationship("Template")
    # referance for the template from which this document has been instanciated from

    def __repr__(self):
        return f"<Document {self.Did}>"
        # simplified string representation of the document 

    def get_info(self):
        return {
            "name":self.master_template.name,
            "description":self.master_template.description,
            "creator":self.owner.fullname,
            "Did":self.Did,
            "href":f"/documents/{self.Did}"
        }
        # return basic info about the document
        # the href property is the URI of the document from the POV of the client-side

    def toJSON(self):
        return {
            "name":self.master_template.name,
            "description":self.master_template.description,
            "creator":self.owner.fullname,
            "Did":self.Did,
            "data":json.loads(self.data),
            "stage":self.stage
        }
        # return a JSON object of the entire content of the document
    
    def advance(self,response_data):
        # This function is called when a user submits changes to a document
        stage = self.stage
        choice = response_data['choice']
        data = response_data["data"]
        # first we seperate data and choice from the response

        nextemail = ""
        completed = False
        try:
            nextemail = data["stations"][stage+1]["Email"]
        except IndexError:
            completed = True
        # compute the next email for the document to go to
        # if an IndexError is thrown that means that the document has reached the end of its path

        origintemplate = self.master_template
        stats = json.loads(origintemplate.stats)
        stats[f"Stage #{stage}"] -= 1
        # load the statistics of the master template of the document
        # decrement the count of the current stage, no matter the choice of the user the document is no longer there.
        
        if choice == "rejected":
            stats["failed"]+=1
            nextemail = ""
            data['stations'][stage]['state'] = 'border-danger'
            fail_email_send(self.owner)
            # if the user chose to reject the document we update the information as above and send out a rejected document email msg
        else:
            # otherwise, color the current stage as passed
            data['stations'][stage]['state'] = 'border-success'
            if completed:
                stats["completed"]+=1
                complition_email_send(self.owner)
            else:
                data['stations'][stage+1]['state'] = 'border-warning'
                stats[f"Stage #{stage+1}"] += 1
            # if the document has been completed we need to send out and email
            # either way, we update the statistics of the master template
            

        self.data = json.dumps(data)
        self.stage += 1
        self.currentemail = nextemail
        origintemplate.stats = json.dumps(stats)
        # to finish we change the data of the document and its master template
        # and finish.
