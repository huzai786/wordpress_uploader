"""added image field in question

Revision ID: 869d3a3169e0
Revises: 82029217cdba
Create Date: 2022-11-04 09:20:25.885006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '869d3a3169e0'
down_revision = '82029217cdba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_category_wp_id'), 'category', ['wp_id'], unique=True)
    op.create_index(op.f('ix_keyword_wp_id'), 'keyword', ['wp_id'], unique=True)
    op.add_column('question', sa.Column('question_image', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('question', 'question_image')
    op.drop_index(op.f('ix_keyword_wp_id'), table_name='keyword')
    op.drop_index(op.f('ix_category_wp_id'), table_name='category')
    # ### end Alembic commands ###