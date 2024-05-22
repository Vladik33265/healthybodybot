"""LETS GO

Revision ID: 45c3f9474524
Revises: 1bc9d452a9d8
Create Date: 2024-05-22 13:29:45.658282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45c3f9474524'
down_revision: Union[str, None] = '1bc9d452a9d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tg_id', sa.Integer(), nullable=True),
    sa.Column('tg_username', sa.String(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone_number'),
    sa.UniqueConstraint('tg_id'),
    sa.UniqueConstraint('tg_username')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'count',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               nullable=True)
    op.alter_column('products', 'price',
               existing_type=sa.Float(),
               type_=sa.TEXT(),
               nullable=True)
    op.alter_column('products', 'description',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               nullable=True)
    op.alter_column('products', 'brand',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               nullable=True)
    op.alter_column('products', 'name',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               nullable=True)
    op.alter_column('products', 'id',
               existing_type=sa.Integer(),
               type_=sa.TEXT(),
               nullable=True,
               autoincrement=True)
    op.drop_table('users')
    # ### end Alembic commands ###