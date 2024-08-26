"""empty message

Revision ID: mtc26082122
Revises: 9acdee3328d1
Create Date: 2024-08-26 12:12:36.462290

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'mtc26082122'  # Updated revision identifier
down_revision = '9acdee3328d1'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('documents', sa.Column('vocabs', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('documents', 'vocabs')