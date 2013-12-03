from wwwpy import db
from werkzeug import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    pwdhash = db.Column(db.String(160))
    last_login = db.Column(db.DateTime)
    last_last_login = db.Column(db.DateTime)
    owned_trees = db.relationship('ChristmasTree', backref = 'owner', lazy = 'dynamic')
    subscribed_trees = db.relationship('ChristmasTree', secondary='user_trees', backref = db.backref('subscriber', lazy = 'dynamic'), lazy = 'dynamic')

    def __init__(self, nickname, email, password):
        self.nickname = nickname
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    def subscribe_to_tree(self, tree):
        self.subscribed_trees.append(tree)
        db.session.commit()

    def get_all_trees(self):
        all_trees = []
        for tree in self.owned_trees:
            tree.owned = True
            all_trees.append(tree)
        for tree in self.subscribed_trees:
            tree.owned = False
            all_trees.append(tree)

        return all_trees


class ChristmasTree(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(255))
    code_name = db.Column(db.String(100))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subscribed_users = db.relationship('User', secondary='user_trees', backref = db.backref('christmas_tree', lazy = 'dynamic'), lazy = 'dynamic')

    def __init__(self, name, description, code_name, owner_id):
        self.name = name
        self.description = description
        self.code_name = code_name
        self.owner_id = owner_id

    def __repr__(self):
        return '<Tree %r>' % (self.name)

user_trees = db.Table('user_trees',
    db.Column('id', db.Integer, primary_key = True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('tree_id', db.Integer, db.ForeignKey('christmas_tree.id')),
    db.Column('date_joined', db.DateTime)
)
