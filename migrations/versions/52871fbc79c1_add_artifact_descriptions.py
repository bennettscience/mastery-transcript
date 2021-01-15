"""add artifact descriptions

Revision ID: 52871fbc79c1
Revises: d0c11127f99b
Create Date: 2021-01-14 19:59:18.588950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "52871fbc79c1"
down_revision = "d0c11127f99b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("artifact", sa.Column("description", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("artifact", "description")
    # ### end Alembic commands ###
