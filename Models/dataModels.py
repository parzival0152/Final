from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    Uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    pwd = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    fullName = db.Column(db.String(255))

    def __repr__(self) -> str:
        return f"Uid:{self.Uid}\nUsername:{self.username}\nemail:{self.email}\npassword:{self.pwd}\nFullname:{self.fullName}"


class Template(db.Model):
    __tablename__ = "templates"
    Tid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    owner = db.Column(db.Integer, db.ForeignKey("users.Uid"))
    data = db.Column(db.JSON, nullable=False)
    stats = db.Column(db.JSON, nullable=False)


class Document(db.Model):
    __tablename__ = "documets"
    Did = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey("users.Uid"))
    master = db.Column(db.Integer, db.ForeignKey("templates.Tid"))
    stage = db.Column(db.Integer)