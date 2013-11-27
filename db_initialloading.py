#!flask/bin/python
from wwwpy import db, models

u = models.User(nickname='sylvain', email='sylvain@emery.sc', password='toto')
db.session.add(u)
db.session.commit()
