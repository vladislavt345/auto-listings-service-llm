"""Create initial users and cars schema.

Revision ID: 20260302_01
Revises:
Create Date: 2026-03-02
"""

from alembic import op
import sqlalchemy as sa

revision = "20260302_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Apply initial schema migration."""

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "cars",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("make", sa.String(length=100), nullable=False),
        sa.Column("model", sa.String(length=100), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(12, 2), nullable=False),
        sa.Column("color", sa.String(length=50), nullable=False),
        sa.Column("source_url", sa.String(length=500), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source_url", name="uq_cars_source_url"),
    )
    op.create_index("ix_cars_id", "cars", ["id"], unique=False)
    op.create_index("ix_cars_make", "cars", ["make"], unique=False)
    op.create_index("ix_cars_model", "cars", ["model"], unique=False)
    op.create_index("ix_cars_year", "cars", ["year"], unique=False)
    op.create_index("ix_cars_price", "cars", ["price"], unique=False)
    op.create_index("ix_cars_color", "cars", ["color"], unique=False)
    op.create_index("ix_cars_source_url", "cars", ["source_url"], unique=True)


def downgrade() -> None:
    """Rollback initial schema migration."""

    op.drop_index("ix_cars_source_url", table_name="cars")
    op.drop_index("ix_cars_color", table_name="cars")
    op.drop_index("ix_cars_price", table_name="cars")
    op.drop_index("ix_cars_year", table_name="cars")
    op.drop_index("ix_cars_model", table_name="cars")
    op.drop_index("ix_cars_make", table_name="cars")
    op.drop_index("ix_cars_id", table_name="cars")
    op.drop_table("cars")

    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
