import json
from os import environ
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import login_required, LoginManager, current_user, login_user, logout_user # library imports

from Models.forms import SigninForm,SignupForm
from Models.dataModels import db,User,Template,Document #personally made imports

load_dotenv() # loading the variables from the .env file

DBFILENAME = environ['DBFILENAME'] # creating the app 
app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False # initializing config
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DBFILENAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = "hello"

Bootstrap(app) # initalizing extensions
db.init_app(app)
loginmanager = LoginManager()
loginmanager.init_app(app)
loginmanager.login_view = "signin"

@loginmanager.user_loader # user loading function
def load_user(user_id):
    return User.query.get(int(user_id))

# HTML endpoints
# these are urls in the webserver that responde to the user with HTML pages and thus render output to the screen

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    return render_template("index.html")

@app.route("/home")
@login_required
def home():
    if not current_user.is_authenticated:
        return redirect(url_for("index"))
    return render_template("home.html",name = current_user.fullname)

@app.route("/preferances", methods = ['POST','GET'])
@login_required
def preferances():
    if request.method == 'GET':
        return render_template("preferances.html",preferances = json.loads(current_user.preferances))
    else:
        current_user.update_preferances(request.form.items())
        db.session.commit()
        return redirect(url_for("home"))

@app.route("/signin", methods = ['POST','GET'])
def signin():

    if current_user.is_authenticated: # a logged in user should not need to login again
        return redirect(url_for("home"))

    form = SigninForm()
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        signingIn = User.query.filter_by(username=username,password = password).first() # get the first user with the combination username and password that where entered, usernames are unique thus if the password is correct we will have only 1 user
        if signingIn is None: # this means that no user was found
            return render_template("signin.html",form = form,found = False,msg = f"Username or password incorrect")
        else:
            login_user(signingIn) # login and redirect home
            return redirect(url_for("home"))
    else:
        return render_template("signin.html",form = form,found = True,msg = "")

@app.route("/signup", methods = ['POST','GET'])
def signup():

    if current_user.is_authenticated: # a logged in user should not need to signup again
        return redirect(url_for("home"))

    if request.method == 'POST':
        count = User.query.filter((User.email == request.form.get("email")) | (User.username == request.form.get("username"))).count()
        # check if there are any users with the same username or same email and prevent them from signing up
        if count !=0:
            form = SignupForm()
            return render_template("signup.html",form = form,err = True,msg = f"Username or Email are already in use")

        newuser = User(
            username=request.form.get("username"),
            fullname=request.form.get("fullname"),
            email=request.form.get("email"),
            password=request.form.get("password")
        )
        db.session.add(newuser)
        db.session.commit()
        login_user(newuser)
        return redirect(url_for("home"))

    else:
        form = SignupForm()
        return render_template("signup.html",form = form)

@app.route('/Mytemplates')
@login_required
def my_templates():
    mode = request.args.get("mode", default="none") # check the path mode
    return render_template("templates.html", mode = mode)

@app.route('/Mydocuments')
@login_required
def my_documents():
    return render_template("forms.html")

@app.route('/templates/<id>')
@login_required
def templates(id):
    if(id=="0"):
        return render_template("templateMaker.html")
    else:
        template = Template.query.get(id)
        return render_template("templateview.html",id = id,viewstats = template.owner.id==current_user.id)

@app.route('/documents/<id>', methods = ['POST','GET'])
@login_required
def documents(id):
    if request.method == "GET":
        document = Document.query.get(id)
        return render_template("documentview.html",id = id, allowed = document.currentemail == current_user.email)
    else: 
        document = Document.query.get(id)
        current_user.past_documents.append(document)
        document.advance(request.json)
        db.session.commit()
        return redirect(url_for("my_documents"))

@app.route('/CreateDocument/<id>')
@login_required
def createdocument(id):
    template = Template.query.get(id)
    newDoc = template.instanciate(current_user)
    db.session.add(newDoc)
    db.session.commit()
    return redirect(url_for("documents",id=newDoc.Did))

@app.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for("index"))

# json endpoint start here
# there functions differ from the ones above as these functions return JSON objects rather then HTML
# thus these are used as and 'api' of sort for clients such as the email subsystem and some front end features.

@app.route('/api/users')
def api_users():
    users = [u.get_info() for u in User.query.all()]
    return jsonify(users)

@app.route('/api/docs_count/<user_id>')
def api_count_of_docs_for_user(user_id):
    user = User.query.get(user_id)
    docs = len(user.pending_documents)
    return jsonify({"count":docs})

@app.route('/api/templates_user/<user_id>')
def api_templates_user(user_id):
    user = User.query.get(user_id)
    return jsonify([temp.get_info() for temp in user.created_templates])

@app.route('/api/templates_all')
def api_templates_all():
    return jsonify([temp.get_info() for temp in Template.query.all()])

@app.route('/api/docs_pending/<user_id>')
def api_docs_pending(user_id):
    user = User.query.get(user_id)
    return jsonify([doc.get_info() for doc in user.pending_documents])

@app.route('/api/docs_past/<user_id>')
def api_docs_past(user_id):
    user = User.query.get(user_id)
    return jsonify([doc.get_info() for doc in user.past_documents])

@app.route('/api/docs_created/<user_id>')
def api_docs_created(user_id):
    user = User.query.get(user_id)
    return jsonify([doc.get_info() for doc in user.created_documents])

@app.route('/api/templates/<Tid>')
def api_templates(Tid):
    return jsonify(Template.query.get(Tid).toJSON())

@app.route('/api/documents/<Did>')
def api_documents(Did):
    return jsonify(Document.query.get(Did).toJSON())

@app.route('/api/current_user_id')
def api_current_user_id():
    if not current_user.is_authenticated: return jsonify({'message':"you are not authenticated"}),401
    return jsonify({
        'id':current_user.id
    })

@app.route("/api/create_template", methods = ['POST'])
def api_create_template():
    template_data = request.json
    tem1 = Template(
        owner=current_user,
        form_response=template_data
    )
    db.session.add(tem1)
    db.session.commit()
    return redirect(url_for("my_templates"))

@app.route("/api/test", methods = ['POST'])
def apitest():
    with open('test.json','w') as f:
        f.write(json.dumps(request.json))
    return redirect(url_for("home"))

@app.route('/purgedatabase')
def purge():
    db.drop_all()
    db.create_all()
    ilay = User( 
        username = "tzuberi",
        password = "123456",
        email = "ilay.tzu@gmail.com",
        fullname = "Ilay Tzuberi"
    )
    omri = User(
        username = "obaron",
        password = "123456",
        email = "obaron4120@gmail.com",
        fullname = "Omri Baron"
    )
    a = User( 
        username = "aaaa",
        password = "123456",
        email = "a@a.com",
        fullname = "Aran Arias"
    )
    b = User( 
        username = "bbbb",
        password = "123456",
        email = "b@b.com",
        fullname = "Betty Bean"
    )
    c = User( 
        username = "cccc",
        password = "123456",
        email = "c@c.com",
        fullname = "Cody Coon"
    )

    db.session.add_all((ilay,omri,a,b,c))
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
