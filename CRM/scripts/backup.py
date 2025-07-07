import os
import shutil
import datetime

CONFIG_PATH = 'config/settings.yaml'
DB_PATH = 'test.db'
BACKUP_DIR = 'backups'

os.makedirs(BACKUP_DIR, exist_ok=True)


def _ts(name: str) -> str:
    ts = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    return os.path.join(BACKUP_DIR, f'{name}_{ts}.bak')


def backup_settings() -> str:
    dest = _ts('settings')
    shutil.copy(CONFIG_PATH, dest)
    return dest


def backup_database() -> str:
    if os.path.exists(DB_PATH):
        dest = _ts('database')
        shutil.copy(DB_PATH, dest)
        return dest
    return ''


def backup_secrets() -> str:
    # placeholder: copy secrets file if exists
    secrets_file = os.path.join('config', 'secrets.env')
    if os.path.exists(secrets_file):
        dest = _ts('secrets')
        shutil.copy(secrets_file, dest)
        return dest
    return ''


def backup_system() -> str:
    """Create an archive of the whole application directory."""
    base = _ts('system')
    archive = shutil.make_archive(base, 'zip', root_dir='.')
    return archive


def backup_data_incremental(data_dir: str = 'data') -> str:
    """Create an archive of the data directory for incremental backups."""
    base = _ts('data_inc')
    archive = shutil.make_archive(base, 'zip', root_dir=data_dir)
    return archive


if __name__ == '__main__':
    print('Settings:', backup_settings())
    print('Database:', backup_database())
    print('Secrets:', backup_secrets())
    print('System:', backup_system())
