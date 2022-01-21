"""empty message

Revision ID: c9447a184c14
Revises: c7044d3a41cb
Create Date: 2022-01-13 18:16:10.463008

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c9447a184c14'
down_revision = 'c7044d3a41cb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('oauth_users',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('oauth_id', sa.String(length=255), nullable=False),
    sa.Column('oauth_name', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['auth.users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('oauth_id', 'oauth_name', name='uniq_oauth_id_name'),
    schema='auth'
    )


def downgrade():
    op.drop_table('oauth_users', schema='auth')
