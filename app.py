import json,os
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length



app = Flask(__name__)
Bootstrap(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SECRET_KEY"] = "hello"
db = SQLAlchemy(app)

class SigninForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(),Length(min = 4, max= 30)])
    password = PasswordField("password", validators=[InputRequired(),Length(min=4,max=50)])

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(),Length(min = 4, max= 30)])
    fullname = StringField("Fullname", validators=[InputRequired(),Length(min = 4, max= 255)])
    email = EmailField("Email", validators=[InputRequired(),Length(min = 4, max= 255)])
    password = PasswordField("Password", validators=[InputRequired(),Length(min=4,max=50)])



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


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    docs = Document.query.filter_by(owner=session['Uid']).all()
    return render_template("home.html",name = session['name'],number = len(docs))

@app.route("/signin", methods = ['POST','GET'])
def signin():
    form = SigninForm()
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        signinngIn = User.query.filter_by(username=username,pwd = password).first()
        if signinngIn is None:
            return render_template("signin.html",form = form,found = False,msg = f"Username or password incorrect")
        else:
            print(signinngIn)
            session['name'] = signinngIn.fullName
            session['Uid'] = signinngIn.Uid
            return redirect(url_for("home"))
    else:
        return render_template("signin.html",form = form,found = True,msg = "")


@app.route("/signup", methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        Uname = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        fullname = request.form.get("fullname")
        
        newuser = User(
            username = Uname,
            email = email,
            pwd = password,
            fullName = fullname
        )
        db.session.add(newuser)
        db.session.commit()

        print(f"commited to database a new user: \n{newuser}\nRedirecting...")
        return redirect(url_for("signin"))

    else:
        form = SignupForm()
        return render_template("signup.html",form = form)

@app.route('/Mytemplates')
def myTemplates():
    # temps = [(i, f"this is the template #{i}") for i in range(1,11)]
    temps = Template.query.filter_by(owner = session["Uid"]).all()
    temps = [{"name":t.name, "description":t.description, "Tid":t.Tid} for t in temps]
    temps.append({"name":"Create new template", "description":"press here to create a new template", "Tid":0})
    return render_template("templates.html",templates = temps)

@app.route('/templates/<id>')
def templates(id):
    return f"""
    <center>
		<h2>Not Implemented <a href="/">Go back</a></h2>
        <h4>{id}</h4>
	</center>
    """


@app.route('/signout')
@app.route('/forms')
def notimplemented():
    return """
    <center>
		<h2>Not Implemented <a href="/">Go back</a></h2>
	</center>
    """


@app.route('/purgedatabase')
def purge():
    os.remove("test.db")
    db.create_all()
    ilay = User(
        username = "tzuberi",
        pwd = "123456",
        email = "ilay.tzu@gmail.com",
        fullName = "Ilay Tzuberi"
    )
    omri = User(
        username = "obaron",
        pwd = "123456",
        email = "obaron4120@gmail.com",
        fullName = "Omri Baron"
    )
    jsonNone = json.dumps(None)
    tem1 = Template(
        name = "test template 1",
        description = "this is some description",
        owner = 1,
        data = jsonNone,
        stats = jsonNone
    )
    tem2 = Template(
        name = "test template 2",
        description = "this is some description",
        owner = 2,
        data = jsonNone,
        stats = jsonNone
    )

    db.session.add_all((ilay,omri,tem1,tem2))
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
