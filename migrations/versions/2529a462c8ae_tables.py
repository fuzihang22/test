"""tables

Revision ID: 2529a462c8ae
Revises: 23e23289d6a3
Create Date: 2023-08-15 12:52:57.563697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2529a462c8ae'
down_revision = '23e23289d6a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('listing',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.Column('food_quantity', sa.Float(), nullable=True),
    sa.Column('food_item', sa.String(), nullable=True),
    sa.Column('address_for_pickup', sa.String(), nullable=True),
    sa.Column('abn', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('phone_number', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('address', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('buisness_name', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('type_of_buisness', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('abn', sa.String(length=64), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('abn')
        batch_op.drop_column('type_of_buisness')
        batch_op.drop_column('buisness_name')
        batch_op.drop_column('address')
        batch_op.drop_column('phone_number')
        batch_op.drop_column('email')

    op.drop_table('listing')
    # ### end Alembic commands ###