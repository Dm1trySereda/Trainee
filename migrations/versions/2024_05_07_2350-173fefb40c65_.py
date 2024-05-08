"""empty message

Revision ID: 173fefb40c65
Revises: 30e95078f630
Create Date: 2024-05-07 23:50:42.646411

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "173fefb40c65"
down_revision: Union[str, None] = "30e95078f630"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "books",
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("book_num", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("author", sa.String(length=255), nullable=False),
        sa.Column(
            "price_new", sa.DECIMAL(precision=10, scale=2), nullable=True
        ),
        sa.Column(
            "price_old", sa.DECIMAL(precision=10, scale=2), nullable=True
        ),
        sa.Column("discount", sa.String(length=20), nullable=True),
        sa.Column("rating", sa.DECIMAL(precision=4, scale=2), nullable=True),
        sa.Column("image", sa.String(length=255), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "books_history",
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("book_num", sa.BigInteger(), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("price", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["book_id"],
            ["books.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("books_history")
    op.drop_table("books")
    # ### end Alembic commands ###