"""point recordings.user_id -> user.id

Revision ID: d594fa31148e
Revises: 0085ae61f8e1
Create Date: 2025-08-08 14:26:07.952585

"""
from alembic import op
import sqlalchemy as sa

revision = 'd594fa31148e'
down_revision = '0085ae61f8e1'
branch_labels = None
depends_on = None

def upgrade():
    # Drop any existing FK on recordings.user_id (name may vary)
    op.drop_constraint('recordings_user_id_fkey', 'recordings', type_='foreignkey')
    # Recreate FK to users.id
    op.create_foreign_key(
        'recordings_user_id_fkey',
        source_table='recordings',
        referent_table='users',
        local_cols=['user_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )

def downgrade():
    op.drop_constraint('recordings_user_id_fkey', 'recordings', type_='foreignkey')
    op.create_foreign_key(
        'recordings_user_id_fkey',
        source_table='recordings',
        referent_table='users',   # if you previously had "user", you can put it here
        local_cols=['user_id'],
        remote_cols=['id']
    )
