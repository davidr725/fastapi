"""add content column to posts table

Revision ID: d62f72133d42
Revises: f1633dccf401
Create Date: 2023-10-24 13:29:39.486105

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd62f72133d42'
down_revision: Union[str, None] = 'f1633dccf401'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
