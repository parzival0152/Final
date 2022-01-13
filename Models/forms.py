from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length

class SigninForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(),Length(min = 4, max= 30)])
    password = PasswordField("password", validators=[InputRequired(),Length(min=4,max=50)])

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(),Length(min = 4, max= 30)])
    fullname = StringField("Fullname", validators=[InputRequired(),Length(min = 4, max= 255)])
    email = EmailField("Email", validators=[InputRequired(),Length(min = 4, max= 255)])
    password = PasswordField("Password", validators=[InputRequired(),Length(min=4,max=50)])