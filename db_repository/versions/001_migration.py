from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
machine = Table('machine', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('host_name', Text),
    Column('host_ip', Text),
    Column('host_address', Text),
    Column('ssh_username', Text),
    Column('ssh_password', Text),
    Column('ssh_port', Integer),
)

task = Table('task', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', Text),
    Column('description', Text),
    Column('cmd', Text),
    Column('params', Text),
    Column('switches', Text),
    Column('arguments', Text),
    Column('stage', Text),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['machine'].create()
    post_meta.tables['task'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['machine'].drop()
    post_meta.tables['task'].drop()
