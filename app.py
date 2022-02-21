import json,os
from pickle import FALSE
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import login_required, LoginManager, current_user, login_user, logout_user
from Models.forms import *
from Models.dataModels import *

jsonNone = json.dumps(None)
dbfilename = "test.db"
app = Flask(__name__)
loginmanager = LoginManager()

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{dbfilename}"
app.config["SECRET_KEY"] = "hello"

Bootstrap(app)
db.init_app(app)
loginmanager.init_app(app)
loginmanager.login_view = "signin"

@loginmanager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
@login_required
def home():
    docs = Document.query.filter_by(owner=current_user.id).all()
    if not current_user.is_authenticated:
        return redirect(url_for("index"))
    return render_template("home.html",name = current_user.fullName,number = len(docs))

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
            login_user(signinngIn)
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
        login_user(newuser)
        print(f"commited to database a new user: \n{newuser}\nRedirecting...")
        return redirect(url_for("home"))

    else:
        form = SignupForm()
        return render_template("signup.html",form = form)

@app.route('/Mytemplates')
def myTemplates():
    temps = Template.query.filter_by(owner = current_user.id).all()
    temps = [{"name":t.name, "description":t.description, "Tid":t.Tid} for t in temps]
    temps.append({"name":"Create new template", "description":"press here to create a new template", "Tid":0})
    return render_template("templates.html",templates = temps)

@app.route('/Myforms')
def myForms():
    return render_template("forms.html")

@app.route('/templates/<id>')
def templates(id):
    if(id=="0"):
        return render_template("templateMaker.html")
    else:
        return f"""
    <center>
		<h2>Not Implemented <a href="/home">Go back</a></h2>
        <h4>{id}</h4>
	</center>
    """


@app.route('/signout')
def signout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/purgedatabase')
def purge():
    os.remove(dbfilename)
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
