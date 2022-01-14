"""empty message

Revision ID: 92dc76b700b2
Revises: 90250bc96dc9
Create Date: 2022-01-14 16:14:24.897262

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '92dc76b700b2'
down_revision = '90250bc96dc9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_master',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('login', sa.String(length=250), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(length=250), nullable=True),
    sa.Column('last_name', sa.String(length=250), nullable=True),
    sa.Column('email', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='auth',
    postgresql_partition_by='HASH (id)'
    )

    op.execute("""
        CREATE TABLE users_master_0 PARTITION OF auth.users_master FOR VALUES WITH (MODULUS 4, REMAINDER 0);
        CREATE TABLE users_master_1 PARTITION OF auth.users_master FOR VALUES WITH (MODULUS 4, REMAINDER 1);
        CREATE TABLE users_master_2 PARTITION OF auth.users_master FOR VALUES WITH (MODULUS 4, REMAINDER 2);
        CREATE TABLE users_master_3 PARTITION OF auth.users_master FOR VALUES WITH (MODULUS 4, REMAINDER 3);
    """)

    op.execute("""
        INSERT INTO auth.users_master (id, created_at, updated_at, login, password, first_name, last_name, email)
            SELECT id, created_at, updated_at, login, password, first_name, last_name, email
            FROM auth.users;
    """)

    op.execute("""
        ALTER TABLE auth.user_role DROP CONSTRAINT user_role_user_id_fkey;
        ALTER TABLE auth.auth_history_master DROP CONSTRAINT auth_history_master_user_id_fkey;
        ALTER TABLE auth.oauth_users DROP CONSTRAINT oauth_users_user_id_fkey;
    """)

    op.execute("""
        ALTER TABLE auth.user_role ADD CONSTRAINT user_role_user_id_fkey FOREIGN KEY(user_id) REFERENCES auth.users_master (id) ON DELETE CASCADE;
        ALTER TABLE auth.auth_history_master ADD CONSTRAINT auth_history_master_user_id_fkey FOREIGN KEY(user_id) REFERENCES auth.users_master (id) ON DELETE CASCADE;
        ALTER TABLE auth.oauth_users ADD CONSTRAINT oauth_users_user_id_fkey FOREIGN KEY(user_id) REFERENCES auth.users_master (id) ON DELETE CASCADE;
    """)

    op.drop_table('users', schema='auth')


def downgrade():
    op.create_table('users',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('login', sa.String(length=250), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(length=250), nullable=True),
    sa.Column('last_name', sa.String(length=250), nullable=True),
    sa.Column('email', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='auth',
    )

    op.execute("""
        INSERT INTO auth.users (id, created_at, updated_at, login, password, first_name, last_name, email)
            SELECT id, created_at, updated_at, login, password, first_name, last_name, email
            FROM auth.users_master;
    """)

    op.execute("""
        DROP TABLE IF EXISTS auth."users_master_0";
        DROP TABLE IF EXISTS auth."users_master_1";
        DROP TABLE IF EXISTS auth."users_master_2";
        DROP TABLE IF EXISTS auth."users_master_3";
    """)

    op.execute("""
        ALTER TABLE auth.user_role DROP CONSTRAINT user_role_user_id_fkey;
        ALTER TABLE auth.auth_history_master DROP CONSTRAINT auth_history_master_user_id_fkey;
        ALTER TABLE auth.oauth_users DROP CONSTRAINT oauth_users_user_id_fkey;
    """)

    op.execute("""
        ALTER TABLE auth.user_role ADD CONSTRAINT user_role_user_id_fkey FOREIGN KEY(user_id) REFERENCES auth.users (id);
        ALTER TABLE auth.auth_history_master ADD CONSTRAINT auth_history_master_user_id_fkey FOREIGN KEY(user_id) REFERENCES auth.users (id);
        ALTER TABLE auth.oauth_users ADD CONSTRAINT oauth_users_user_id_fkey FOREIGN KEY(user_id) REFERENCES auth.users (id);
    """)

    op.drop_table('users_master', schema='auth')
