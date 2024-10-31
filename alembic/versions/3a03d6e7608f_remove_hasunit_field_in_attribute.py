"""remove hasUnit field in attribute

Revision ID: 3a03d6e7608f
Revises: aa955cc3c5cc
Create Date: 2024-10-30 16:26:18.416257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a03d6e7608f'
down_revision: Union[str, None] = 'aa955cc3c5cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('attribute', 'has_unit')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('attribute', sa.Column('has_unit', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###