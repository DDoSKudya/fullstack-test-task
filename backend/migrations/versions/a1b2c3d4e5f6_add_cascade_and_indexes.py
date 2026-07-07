"""add cascade and indexes

Revision ID: a1b2c3d4e5f6
Revises: 0d6439d2e79f
Create Date: 2026-07-07 19:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

revision: str = "a1b2c3d4e5f6"
down_revision: str | Sequence[str] | None = "0d6439d2e79f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint("alerts_file_id_fkey", "alerts", type_="foreignkey")
    op.create_foreign_key(
        "fk_alerts_file_id",
        "alerts",
        "files",
        ["file_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index("ix_alerts_file_id", "alerts", ["file_id"])
    op.create_index(
        "ix_files_created_at",
        "files",
        ["created_at"],
        postgresql_ops={"created_at": "DESC"},
    )
    op.create_index(
        "ix_alerts_created_at",
        "alerts",
        ["created_at"],
        postgresql_ops={"created_at": "DESC"},
    )


def downgrade() -> None:
    op.drop_index("ix_alerts_created_at", table_name="alerts")
    op.drop_index("ix_files_created_at", table_name="files")
    op.drop_index("ix_alerts_file_id", table_name="alerts")
    op.drop_constraint("fk_alerts_file_id", "alerts", type_="foreignkey")
    op.create_foreign_key(
        "alerts_file_id_fkey",
        "alerts",
        "files",
        ["file_id"],
        ["id"],
    )
