from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user_tree_subscriptions = Table('user_tree_subscriptions', post_meta,
    Column('user_id', Integer, primary_key=True, nullable=False),
    Column('tree_id', Integer, primary_key=True, nullable=False),
    Column('date_joined', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user_tree_subscriptions'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user_tree_subscriptions'].drop()
