from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, PasswordField, TextAreaField, HiddenField, validators
from wwwpy.models import User, ChristmasTree
from flask.ext.login import current_user

class LoginForm(Form):
	email = TextField("Email", validators = [validators.Email(), validators.InputRequired()])
	password = PasswordField("Password", validators = [validators.InputRequired()])
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
	nickname = TextField("Nickname", validators = [validators.InputRequired(), validators.Length(min = 4, max = 64)])
	email = TextField("Email", validators = [validators.Email(), validators.InputRequired(), validators.Length(min = 5, max = 120)])
	password = PasswordField("Password", validators = [validators.InputRequired(), validators.Length(min = 4)])
	submit = SubmitField("Create account")

	def validate(self):
		if not Form.validate(self):
			return False

		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user:
			self.email.errors.append("Email already taken")
		else:
			return True

class NewTreeForm(Form):
	name = TextField("Name", validators = [validators.InputRequired(), validators.Length(min = 1, max = 64)])
	description = TextAreaField("Description", validators = [validators.Length(max = 255)])
	submit = SubmitField("Create tree")

	def validate(self):
		if not Form.validate(self):
			return False

		tree = ChristmasTree.query.filter_by(owner_id = current_user.id).filter_by(name = self.name.data).first()
		if tree:
			self.name.errors.append("you've already created a tree with this name")
		else:
			return True

class EditTreeForm(Form):
	name = TextField("Name", validators = [validators.InputRequired(), validators.Length(min = 1, max = 64)])
	description = TextAreaField("Description", validators = [validators.Length(max = 255)])
	id = HiddenField("id")
	submit = SubmitField("Modify tree")

	def validate(self):
		if not Form.validate(self):
			return False

		tree = ChristmasTree.query.filter_by(owner_id = current_user.id).filter_by(name = self.name.data).first()
		if tree and str(tree.id) <> self.id.data:
			self.name.errors.append("you've already created a tree with this name")
		else:
			return True

class NewSubsTreeForm(Form):
	code_name = TextField("Code Name", validators = [validators.InputRequired(), validators.Length(min = 1, max = 100)])
	submit = SubmitField("Subscribe to tree")

	def validate(self):
		if not Form.validate(self):
			return False

		tree = ChristmasTree.query.filter_by(code_name = self.code_name.data).first()
		if tree is None:
			self.code_name.errors.append("ain't no tree with this name")
		else:
			if tree.owner_id == current_user.id:
				self.code_name.errors.append("you can't subscribe to your own tree")
			else:
				if current_user in tree.users:
					self.code_name.errors.append("you have already subscribed to this tree")
				else:
					return True

