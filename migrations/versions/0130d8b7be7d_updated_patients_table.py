"""updated patients table

Revision ID: 0130d8b7be7d
Revises: 52257ec9a7dd
Create Date: 2023-12-19 21:44:02.232820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0130d8b7be7d'
down_revision = '52257ec9a7dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('is_verified', sa.Boolean(), nullable=True))
        batch_op.create_unique_constraint(None, ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('is_verified')
        batch_op.drop_column('password')

    # ### end Alembic commands ###
