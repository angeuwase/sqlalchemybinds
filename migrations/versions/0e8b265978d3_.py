"""empty message

Revision ID: 0e8b265978d3
Revises: fc56aac322ea
Create Date: 2021-06-21 19:18:40.950218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e8b265978d3'
down_revision = 'fc56aac322ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('survey_result',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('survey_result')
    # ### end Alembic commands ###
