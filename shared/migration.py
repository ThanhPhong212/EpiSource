import os
from alembic.config import Config
from alembic import command
from sqlalchemy import inspect
from shared.db import db

def run_migration(app):
    inspector = inspect(db.engine)
    # Check if any tables exist (skip if DB is already initialized)
    if inspector.get_table_names():
        return

    print("⏳ Running first-time Alembic upgrade...")
    alembic_cfg = Config(os.path.abspath("alembic.ini"))
    command.upgrade(alembic_cfg, 'head')
    print("✅ Migration complete.")
