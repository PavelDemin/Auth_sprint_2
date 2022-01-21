"""empty message

Revision ID: bc2a2ad76715
Revises: 5274241b4010
Create Date: 2021-12-29 14:22:31.829992

"""
from datetime import datetime
from uuid import uuid4

import sqlalchemy as sa
from alembic import op

from app.models.role import DefaultRoleEnum

# revision identifiers, used by Alembic.
revision = 'bc2a2ad76715'
down_revision = '5274241b4010'
branch_labels = None
depends_on = None


def upgrade():

    schema='auth'

    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect(only=('roles',), schema=schema)
    roles_table = sa.Table('roles', meta, schema=schema)
    op.bulk_insert(
        roles_table,
        [
            {
                'id': str(uuid4()),
                'name': DefaultRoleEnum.user.value,
                'description': "has basic permissions.",
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
            },
            {
                'id': str(uuid4()),
                'name': DefaultRoleEnum.staff.value,
                'description': '',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
            },
            {
                'id': str(uuid4()),
                'name': DefaultRoleEnum.admin.value,
                'description': 'has all permissions.',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
            },
        ],
    )


def downgrade():
    pass
