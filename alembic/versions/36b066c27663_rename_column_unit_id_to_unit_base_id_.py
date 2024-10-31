"""rename column unit_id to unit_base_id in attribute

Revision ID: 36b066c27663
Revises: 3a03d6e7608f
Create Date: 2024-10-30 20:32:52.839891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36b066c27663'
down_revision: Union[str, None] = '3a03d6e7608f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename the column `unit_id` to `unit_base_id` while preserving data
    op.alter_column('attribute', 'unit_id', new_column_name='unit_base_id')
    
    # Drop the existing foreign key constraint on the old column name
    op.drop_constraint('attribute_unit_id_fkey', 'attribute', type_='foreignkey')
    
    # Add a new foreign key constraint on the renamed column
    op.create_foreign_key(
        'attribute_unit_base_id_fkey',  # name of the new foreign key constraint
        'attribute',                    # source table
        'unit',                         # destination table
        ['unit_base_id'],               # source column(s)
        ['id']                          # destination column(s)
    )


def downgrade() -> None:
    # Rename the column `unit_base_id` back to `unit_id` to revert to the original
    op.alter_column('attribute', 'unit_base_id', new_column_name='unit_id')
    
    # Drop the foreign key constraint on `unit_base_id`
    op.drop_constraint('attribute_unit_base_id_fkey', 'attribute', type_='foreignkey')
    
    # Recreate the original foreign key constraint on `unit_id`
    op.create_foreign_key(
        'attribute_unit_id_fkey',       # name of the original foreign key constraint
        'attribute',                    # source table
        'unit',                         # destination table
        ['unit_id'],                    # source column(s)
        ['id']                          # destination column(s)
    )