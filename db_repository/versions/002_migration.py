from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
product = Table('product', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', Text),
    Column('language', Text),
    Column('framework', Text),
    Column('deploy_steps', Text),
    Column('maintain_steps', Text),
)

project = Table('project', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', Text),
    Column('client_name', Text),
    Column('product_type', Text),
    Column('server_id', Integer),
    Column('instance_port', Integer),
    Column('project_dir', Text),
    Column('vcs_tool', Text),
    Column('vcs_repo', Text),
    Column('mysql_db_name', Text),
)

machine = Table('machine', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('host_name', Text),
    Column('host_ip', Text),
    Column('host_address', Text),
    Column('ssh_username', Text),
    Column('ssh_password', Text),
    Column('ssh_port', Integer),
    Column('mysql_username', Text),
    Column('mysql_password', Text),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('email', String(length=255), nullable=False),
    Column('confirmed_at', DateTime),
    Column('is_active', Boolean, nullable=False),
    Column('first_name', String(length=50), nullable=False),
    Column('last_name', String(length=50), nullable=False),
    Column('svn_username', Text),
    Column('svn_password', Text),
    Column('git_username', Text),
    Column('git_password', Text),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['product'].create()
    post_meta.tables['project'].create()
    post_meta.tables['machine'].columns['mysql_password'].create()
    post_meta.tables['machine'].columns['mysql_username'].create()
    post_meta.tables['user'].columns['git_password'].create()
    post_meta.tables['user'].columns['git_username'].create()
    post_meta.tables['user'].columns['svn_password'].create()
    post_meta.tables['user'].columns['svn_username'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['product'].drop()
    post_meta.tables['project'].drop()
    post_meta.tables['machine'].columns['mysql_password'].drop()
    post_meta.tables['machine'].columns['mysql_username'].drop()
    post_meta.tables['user'].columns['git_password'].drop()
    post_meta.tables['user'].columns['git_username'].drop()
    post_meta.tables['user'].columns['svn_password'].drop()
    post_meta.tables['user'].columns['svn_username'].drop()
