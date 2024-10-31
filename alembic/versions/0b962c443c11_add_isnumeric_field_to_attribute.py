"""add isNumeric field to Attribute

Revision ID: 0b962c443c11
Revises: 8657f82c00cc
Create Date: 2024-10-30 16:16:27.505710

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b962c443c11'
down_revision: Union[str, None] = '8657f82c00cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('attribute', sa.Column('isNumeric', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('attribute', 'isNumeric')
    # ### end Alembic commands ###