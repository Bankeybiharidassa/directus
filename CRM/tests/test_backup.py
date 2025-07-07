import os
from scripts import backup


def test_backup_creates_files(tmp_path, monkeypatch):
    monkeypatch.setattr(backup, 'BACKUP_DIR', tmp_path)
    settings_file = os.path.join(tmp_path, 'settings.yaml')
    with open(settings_file, 'w') as f:
        f.write('test')
    monkeypatch.setattr(backup, 'CONFIG_PATH', settings_file)

    db_file = os.path.join(tmp_path, 'db.sqlite')
    with open(db_file, 'w') as f:
        f.write('db')
    monkeypatch.setattr(backup, 'DB_PATH', db_file)

    path1 = backup.backup_settings()
    path2 = backup.backup_database()

    assert os.path.exists(path1)
    assert os.path.exists(path2)


def test_backup_database_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(backup, "BACKUP_DIR", tmp_path)
    monkeypatch.setattr(backup, "DB_PATH", str(tmp_path / "missing.db"))
    assert backup.backup_database() == ""


def test_backup_system_and_incremental(tmp_path, monkeypatch):
    monkeypatch.setattr(backup, "BACKUP_DIR", tmp_path)

    def fake_make_archive(base_name, format, root_dir="."):
        path = f"{base_name}.{format}"
        open(path, "w").close()
        return path

    monkeypatch.setattr(backup.shutil, "make_archive", fake_make_archive)
    monkeypatch.setattr(backup, "_ts", lambda name: str(tmp_path / name))

    sys_path = backup.backup_system()
    inc_path = backup.backup_data_incremental(data_dir=str(tmp_path))

    assert os.path.exists(sys_path)
    assert os.path.exists(inc_path)
