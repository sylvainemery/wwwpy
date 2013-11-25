from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, validators
 
class LoginForm(Form):
	name = TextField("Name", validators=[validators.Length(min=4, max=25)])
	submit = SubmitField("Login")