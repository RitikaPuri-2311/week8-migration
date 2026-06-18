"""add password column

Revision ID: 86de1aa2e4d6
Revises: bfe0dd323ede
Create Date: 2026-06-17 15:26:21.349806

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86de1aa2e4d6'
down_revision: Union[str, Sequence[str], None] = 'bfe0dd323ede'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('password', sa.String(), nullable=True)
    )

    op.create_unique_constraint(
        'uq_users_email',   # ✅ GIVE IT A NAME
        'users',
        ['email']
    )


def downgrade() -> None:
    op.drop_constraint(
    'users_email_key',   
    'users',
    type_='unique'
)

    op.drop_column('users', 'password')