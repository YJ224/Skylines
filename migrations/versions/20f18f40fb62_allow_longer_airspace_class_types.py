# revision identifiers, used by Alembic.
revision = '20f18f40fb62'
down_revision = '2dade673f10e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('airspace', 'airspace_class',
                    type_=sa.String(12),
                    nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('airspace', 'airspace_class',
                    type_=sa.String(3),
                    nullable=False)
    ### end Alembic commands ###
