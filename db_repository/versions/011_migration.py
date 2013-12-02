from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
christmas_tree = Table('christmas_tree', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('user_id', Integer),
    Column('description', String),
    Column('code_name', String),
)

christmas_tree = Table('christmas_tree', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('description', String(length=255)),
    Column('code_name', String(length=100)),
    Column('owner_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['christmas_tree'].columns['user_id'].drop()
    post_meta.tables['christmas_tree'].columns['owner_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['christmas_tree'].columns['user_id'].create()
    post_meta.tables['christmas_tree'].columns['owner_id'].drop()
