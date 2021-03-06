"""empty message

Revision ID: 2d98469ff172
Revises: 
Create Date: 2021-03-21 12:44:25.668577

"""
from alembic import op
import sqlalchemy as sa

import opentunes_api

# revision identifiers, used by Alembic.
revision = '2d98469ff172'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tracks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('file', sa.String(), nullable=True),
    sa.Column('file_mtime', sa.DateTime(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('bpm', opentunes_api.database.types.DBAgnosticNumeric(), nullable=True),
    sa.Column('key', sa.String(), nullable=True),
    sa.Column('duration', opentunes_api.database.types.DBAgnosticNumeric(), nullable=True),
    sa.Column('bitrate', sa.Integer(), nullable=True),
    sa.Column('album', sa.String(), nullable=True),
    sa.Column('import_error', sa.String(), nullable=True),
    sa.Column('image_files', opentunes_api.database.types.ArrayType(), nullable=True),
    sa.Column('image_import_error', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('file')
    )
    op.create_index(op.f('ix_tracks_id'), 'tracks', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tracks_id'), table_name='tracks')
    op.drop_table('tracks')
    # ### end Alembic commands ###
