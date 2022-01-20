"""empty message

Revision ID: 90250bc96dc9
Revises: c9447a184c14
Create Date: 2022-01-14 13:19:57.251780

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

# revision identifiers, used by Alembic.
revision = '90250bc96dc9'
down_revision = 'c9447a184c14'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table('auth_history_master',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('user_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_agent', sa.Text(), nullable=False),
    sa.Column('ip_address', sqlalchemy_utils.types.ip_address.IPAddressType(length=50), nullable=True),
    sa.Column('device', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['auth.users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'device'),
    schema='auth',
    postgresql_partition_by='LIST (device)'
    )

    op.execute("""
        CREATE TABLE IF NOT EXISTS auth."auth_history_mobile" PARTITION OF auth."auth_history_master" FOR VALUES IN ('mobile');
        CREATE TABLE IF NOT EXISTS auth."auth_history_smart" PARTITION OF auth."auth_history_master" FOR VALUES IN ('smart');
        CREATE TABLE IF NOT EXISTS auth."auth_history_web" PARTITION OF auth."auth_history_master" FOR VALUES IN ('web');""")
    op.execute("""
        INSERT INTO auth.auth_history_master (id, user_id, timestamp, user_agent, ip_address, device)
            SELECT id, user_id, timestamp, user_agent, ip_address, device
            FROM auth.auth_history;
    """)

    op.drop_table('auth_history', schema='auth')


def downgrade():

    op.create_table('auth_history',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('user_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_agent', sa.Text(), nullable=False),
    sa.Column('ip_address', sqlalchemy_utils.types.ip_address.IPAddressType(length=50), nullable=True),
    sa.Column('device', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['auth.users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'device'),
    schema='auth',
    )

    op.execute("""
            INSERT INTO auth.auth_history (id, user_id, timestamp, user_agent, ip_address, device)
                SELECT id, user_id, timestamp, user_agent, ip_address, device
                FROM auth.auth_history_master;
        """)
    op.execute("""
            DROP TABLE IF EXISTS auth."auth_history_mobile";
            DROP TABLE IF EXISTS auth."auth_history_smart";
            DROP TABLE IF  EXISTS auth."auth_history_web";""")

    op.drop_table('auth_history_master', schema='auth')
