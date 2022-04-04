import json,os
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import login_required, LoginManager, current_user, login_user, logout_user
from Models.forms import *
from Models.dataModels import *
from Models.functions import *

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
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    return render_template("index.html")

@app.route("/home")
@login_required
def home():
    #docs = Document.query.filter_by(owner=current_user.id).all()
    if not current_user.is_authenticated:
        return redirect(url_for("index"))
    return render_template("home.html",name = current_user.fullName,number = 0)#len(docs))

@app.route("/signin", methods = ['POST','GET'])
def signin():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

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

    if current_user.is_authenticated:
        return redirect(url_for("home"))

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
@login_required
def myTemplates():
    temps = Template.query.filter_by(owner = current_user.id).all()
    temps = [{"name":t.name, "description":t.description, "Tid":t.Tid} for t in temps]
    temps.append({"name":"Create new template", "description":"press here to create a new template", "Tid":0})
    return render_template("templates.html",templates = temps)

@app.route('/Myforms')
@login_required
def myForms():
    docs = Document.query.filter_by(owner = current_user.id).all()
    docs = [{"name":t.Did, "description":t.owner, "Did":t.Did} for t in docs]
    return render_template("forms.html", MyDocuments = docs)

@app.route('/templates/<id>')
@login_required
def templates(id):
    if(id=="0"):
        return render_template("templateMaker.html")
    else:
        template = Template.query.get(id)
        data = json.loads(template.data)
        stats = json.loads(template.stats)
        return render_template("templateview.html",data = data,id = id,stats = stats,viewstats = template.owner==current_user.id)

@app.route('/documents/<id>', methods = ['POST','GET'])
@login_required
def documents(id):
    if request.method == "GET":
        document = Document.query.get(id)
        data = json.loads(document.data)
        return render_template("documentview.html",data = data,stage = document.stage)
    else:
        pass

@app.route('/createTemplate',methods = ['POST'])
@login_required
def createtemp():
    data,stats = parse_response(request.form.to_dict())
    tem1 = Template(
        name = request.form.get("title"),
        description = request.form.get("description"),
        owner = current_user.id,
        data = data,
        stats = stats
    )
    db.session.add(tem1)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/CreateDocument/<id>')
@login_required
def createdocument(id):
    template = Template.query.get(id)
    stats = json.loads(template.stats)
    stats["created"] += 1
    stats["0"] += 1
    template.stats = json.dumps(stats)
    newDoc = Document(
        data = template.data,
        owner = current_user.id,
        master = template.Tid,
        stage = 0,
        currentemail = current_user.email
    )
    db.session.add(newDoc)
    db.session.commit()
    return redirect(url_for("documents",id=newDoc.Did))

@app.route('/signout')
@login_required
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
    a = User(
        username = "aaaa",
        pwd = "123456",
        email = "a@a.com",
        fullName = "Test User A"
    )
    b = User(
        username = "bbbb",
        pwd = "123456",
        email = "b@b.com",
        fullName = "Test User B"
    )
    c = User(
        username = "cccc",
        pwd = "123456",
        email = "c@c.com",
        fullName = "Test User C"
    )

    db.session.add_all((ilay,omri,a,b,c))
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
