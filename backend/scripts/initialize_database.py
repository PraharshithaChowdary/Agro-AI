"""Initialize AGRO AI's schema and the bundled botanical catalogue.

No demo users, default passwords, or administrator accounts are created. Use the
signup interface to create a normal user account.
"""
from __future__ import annotations
from pathlib import Path
import subprocess
import sys

if __name__ == "__main__":
    script = Path(__file__).resolve().with_name("bootstrap_database.py")
    raise SystemExit(subprocess.call([sys.executable, str(script)]))
