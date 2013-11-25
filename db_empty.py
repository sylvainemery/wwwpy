#!flask/bin/python
from wwwpy import db, models

users = models.User.query.all()
for u in users:
	db.session.delete(u)

db.session.commit()
