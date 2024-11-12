# run_migrations.py
import os

from dotenv import load_dotenv

from alembic import command
from alembic.config import Config

load_dotenv()

def run_migrations():
    alembic_cfg = Config("alembic.ini")

    # Check environment variable to decide if migrations should be run
    if os.getenv("RUN_MIGRATIONS") == "true":
        command.upgrade(alembic_cfg, "head")
        print("Migrations applied.")
    else:
        print("Skipping migrations.")

if __name__ == "__main__":
    run_migrations()