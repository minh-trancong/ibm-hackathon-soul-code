# New Alembic migration script in `backend/alembic/versions/<new_revision_id>.py`
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'mtc-26-08-21-22'
down_revision = '9acdee3328d1'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('documents', sa.Column('vocabs', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('documents', 'vocabs')