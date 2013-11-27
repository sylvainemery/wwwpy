from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, PasswordField, validators
from wwwpy.models import User

class LoginForm(Form):
	email = TextField("Email", validators=[validators.Email(), validators.InputRequired()])
	password = PasswordField("Password", validators=[validators.InputRequired()])
	submit = SubmitField("Login")

	def validate(self):
		if not Form.validate(self):
			return False

		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user and user.check_password(self.password.data):
			return True
		else:
			self.email.errors.append("Invalid email or password")

class NewAccountForm(Form):
	nickname = TextField("Nickname", validators=[validators.InputRequired(), validators.Length(min=4, max=64)])
	email = TextField("Email", validators=[validators.Email(), validators.InputRequired(), validators.Length(min=5, max=120)])
	password = PasswordField("Password", validators=[validators.InputRequired(), validators.Length(min=4)])
	submit = SubmitField("Create account")

	def validate(self):
		if not Form.validate(self):
			return False

		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user:
			self.email.errors.append("Email already taken")
		else:
			return True
