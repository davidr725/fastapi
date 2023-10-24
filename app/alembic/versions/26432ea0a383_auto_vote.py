"""auto-vote

Revision ID: 26432ea0a383
Revises: 11dbc23505a7
Create Date: 2023-10-24 14:07:15.253671

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26432ea0a383'
down_revision: Union[str, None] = '11dbc23505a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'],
                                            ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'],
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id', 'post_id'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###
