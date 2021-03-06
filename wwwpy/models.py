from wwwpy import db
from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    pwdhash = db.Column(db.String(160))
    last_login = db.Column(db.DateTime)
    last_last_login = db.Column(db.DateTime)
    owned_trees = db.relationship('ChristmasTree', backref = 'owner', lazy = 'dynamic')
    subscribed_trees = association_proxy('subs_trees', 'tree')

    def __init__(self, nickname, email, password, **kwargs):
        super(User, self).__init__(**kwargs)
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

    @property
    def all_trees(self):
        all_trees = []
        for s in self.subs_trees:
            t = s.tree
            t.owned = False
            if t.owner_id == self.id:
                t.owned = True
            t.no_hint = False
            if s.hint is None:
                t.no_hint = True
            all_trees.append(t)

        return sorted(set(all_trees), key=lambda tree: tree.fullname)


class ChristmasTree(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(255))
    code_name = db.Column(db.String(100))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    users = association_proxy('subs_users', 'user')

    def __init__(self, name, description, code_name, owner_id, **kwargs):
        super(ChristmasTree, self).__init__(**kwargs)
        self.name = name
        self.description = description
        self.code_name = code_name
        self.owner_id = owner_id

    def __repr__(self):
        return '<Tree %r\%r>' % (self.owner.nickname, self.name)

    @hybrid_property
    def fullname(self):
        return self.owner.nickname + '\\' + self.name


class UserTreeSubscriptions(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    tree_id = db.Column(db.Integer, db.ForeignKey('christmas_tree.id'), primary_key = True)
    date_joined = db.Column(db.DateTime)
    hint = db.Column(db.String(255))
    user = db.relationship('User', backref='subs_trees')
    tree = db.relationship('ChristmasTree', backref='subs_users')

    def __init__(self, tree=None, **kwargs):
        super(UserTreeSubscriptions, self).__init__(**kwargs)
        self.tree = tree
        self.date_joined = datetime.utcnow() #ca me plait pas que ce ne soit que la

    def __repr__(self):
        return '<Tree %r, User %r, hint %r>' % (self.tree.name, self.user.nickname, self.hint)
