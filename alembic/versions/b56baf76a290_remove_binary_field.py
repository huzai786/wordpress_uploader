"""remove binary field

Revision ID: b56baf76a290
Revises: bd4c2c22dd19
Create Date: 2022-11-07 07:41:14.193200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b56baf76a290'
down_revision = 'bd4c2c22dd19'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('question', 'question_image')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('question_image', sa.VARCHAR(), nullable=True))
    # ### end Alembic commands ###
