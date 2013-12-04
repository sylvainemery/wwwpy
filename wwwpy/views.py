from flask import redirect, render_template, request, session, url_for, g, flash, send_from_directory, abort
from wwwpy import app, login_manager, db
from settings import adjectives, nouns
from forms import LoginForm, NewAccountForm, NewTreeForm, EditTreeForm, NewSubsTreeForm
from models import User, ChristmasTree, user_trees
from flask.ext.login import LoginManager, current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required, user_logged_in
import os
from datetime import datetime
from random import choice


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
def index():
    return render_template('index.html')

def handle_login(app, user):
	g.user.last_last_login = g.user.last_login
	g.user.last_login = datetime.utcnow()
	db.session.add(g.user)
	db.session.commit()

user_logged_in.connect(handle_login)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))

	login_form = LoginForm()

	if login_form.validate_on_submit():
		user = User.query.filter_by(email = login_form.email.data).first()
		login_user(user)
		return redirect(request.args.get("next") or url_for("index"))
	else:
		return render_template('login.html', form = login_form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	newaccount_form = NewAccountForm()

	if newaccount_form.validate_on_submit():
		newuser = User(newaccount_form.nickname.data, newaccount_form.email.data, newaccount_form.password.data)
		db.session.add(newuser)
		db.session.commit()
		login_user(newuser)
		return redirect(url_for('my_account', nickname = newuser.nickname))
	else:
		return render_template('signup.html', form = newaccount_form)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def my_account(nickname):
	if nickname <> current_user.nickname:
		abort(403)
	return render_template('useraccount.html')


@app.route('/newtree', methods=['GET', 'POST'])
@login_required
def newtree():
	newtree_form = NewTreeForm()

	if newtree_form.validate_on_submit():
		code_name = get_code_name()
		ntree = ChristmasTree(newtree_form.name.data, newtree_form.description.data, code_name, current_user.id)
		db.session.add(ntree)
		db.session.commit()
		return redirect(url_for('tree', nickname = current_user.nickname, treename = ntree.name))
	else:
		return render_template('newtree.html', form = newtree_form)


@app.route('/subscribetotree', methods=['GET', 'POST'])
@login_required
def subscribetotree():
	substree_form = NewSubsTreeForm()

	if substree_form.validate_on_submit():
		t = ChristmasTree.query.filter_by(code_name = substree_form.code_name.data).first()
		current_user.subscribe_to_tree(t)
		return redirect(url_for('my_account', nickname = current_user.nickname))
	else:
		return render_template('substree.html', form = substree_form)


@app.route('/user/<nickname>/tree/<treename>')
@login_required
def tree(nickname, treename):
	t = db.session.query(ChristmasTree).filter(ChristmasTree.owner.has(nickname = nickname)).filter(ChristmasTree.name == treename).first()
	if t is None:
		abort(404)

	is_owner = False
	if t.owner.id == current_user.id:
		is_owner = True

	is_subscriber = False
	if current_user in t.subscribed_users:
		is_subscriber = True

	if not is_owner and not is_subscriber:
		abort(403)

	return render_template('tree.html', tree = t, is_owner = is_owner)


@app.route('/user/<nickname>/tree/<treename>/edit', methods=['GET', 'POST'])
@login_required
def edittree(nickname, treename):
	if nickname <> current_user.nickname:
		abort(403)

	t = ChristmasTree.query.filter_by(owner_id = current_user.id).filter_by(name = treename).first()
	if t is None:
		abort(404)

	edittree_form = EditTreeForm(obj = t)

	if edittree_form.validate_on_submit():
		edittree_form.populate_obj(t)
		db.session.add(t)
		db.session.commit()
		return redirect(url_for('tree', nickname = current_user.nickname, treename = t.name))

	return render_template('edittree.html', form = edittree_form, tree = t)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(403)
def not_authorized(e):
    return render_template('403.html'), 403


def get_code_name():
	return choice(adjectives).strip() + ' ' + choice(nouns).strip()
