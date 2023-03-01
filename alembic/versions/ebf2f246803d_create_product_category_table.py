"""create product_category table

Revision ID: ebf2f246803d
Revises: ef1d360ab10c
Create Date: 2023-02-23 21:51:58.068066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebf2f246803d'
down_revision = 'ef1d360ab10c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product_category',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.category_id'], name='fk_category_product', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['product_id'], ['products.product_id'], name='fk_product_category', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('product_id', 'category_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_category')
    # ### end Alembic commands ###
