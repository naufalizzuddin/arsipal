"""Prepare persistent storage, schema and static assets before starting the web app."""
import os
from pathlib import Path
import subprocess
import sys


def main():
    Path(os.getenv('DATABASE_PATH', '/app/data/db.sqlite3')).parent.mkdir(
        parents=True, exist_ok=True
    )
    Path(os.getenv('MEDIA_ROOT', '/app/dokumen')).mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, 'manage.py', 'migrate', '--noinput'], check=True)
    subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=True)
    os.execvp(sys.argv[1], sys.argv[1:])


if __name__ == '__main__':
    main()
