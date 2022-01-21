"""empty message

Revision ID: c7044d3a41cb
Revises: d699ff944ccc
Create Date: 2021-12-30 12:59:39.389707

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c7044d3a41cb'
down_revision = 'd699ff944ccc'
branch_labels = None
depends_on = None


def upgrade():

    op.drop_table('auth_history', schema='auth')

    op.create_table('auth_history',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('user_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_agent', sa.Text(), nullable=False),
    sa.Column('ip_address', sqlalchemy_utils.types.ip_address.IPAddressType(length=50), nullable=True),
    sa.Column('device', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['auth.users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'device'),
    schema='auth'
    )


def downgrade():

    op.drop_table('auth_history', schema='auth')

    op.create_table('auth_history',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('user_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_agent', sa.Text(), nullable=False),
    sa.Column('ip_address', sqlalchemy_utils.types.ip_address.IPAddressType(length=50), nullable=True),
    sa.Column('device', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['auth.users.id'], ),
    sa.PrimaryKeyConstraint('id', 'device'),
    schema='auth'
    )
