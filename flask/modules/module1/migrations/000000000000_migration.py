from alembic import op
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '000000000000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('test',
        Column('id', UUID,
               server_default=text('gen_random_uuid()'),
               primary_key=True),
        Column('test', String())
    )


def downgrade():
    op.drop_table('test')