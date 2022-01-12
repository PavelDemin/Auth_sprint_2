"""empty message

Revision ID: d699ff944ccc
Revises: bc2a2ad76715
Create Date: 2021-12-30 11:56:44.904902

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

# revision identifiers, used by Alembic.
revision = 'd699ff944ccc'
down_revision = 'bc2a2ad76715'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_table('user_role', schema='auth')

    op.create_table('user_role',
    sa.Column('user_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True),
    sa.Column('role_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['auth.roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['auth.users.id'], ondelete='CASCADE'),
    sa.UniqueConstraint('user_id', 'role_id', name='uniq_user_role'),
    schema='auth'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_role', schema='auth')

    op.create_table('user_role',
    sa.Column('user_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('role_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['auth.roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['auth.users.id'], ),
    sa.UniqueConstraint('user_id', 'role_id', name='uniq_user_role'),
    schema='auth'
    )

    # ### end Alembic commands ###
