from alembic import op
from sqlalchemy import Column, String


# revision identifiers, used by Alembic.
revision = '000000000000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('test',
        Column('test', String())
    )


def downgrade():
    op.drop_table('test')