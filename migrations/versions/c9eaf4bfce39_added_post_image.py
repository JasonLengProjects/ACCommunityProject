"""added post image

Revision ID: c9eaf4bfce39
Revises: b59615cbc75d
Create Date: 2020-06-22 00:01:21.436544

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c9eaf4bfce39'
down_revision = 'b59615cbc75d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('title', sa.String(length=140), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('blog_post_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_image', sa.String(length=128), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['blog_posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('blog_post')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_post',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('date', mysql.DATETIME(), nullable=False),
    sa.Column('title', mysql.VARCHAR(length=140), nullable=False),
    sa.Column('text', mysql.TEXT(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='blog_post_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('blog_post_image')
    op.drop_table('blog_posts')
    # ### end Alembic commands ###
