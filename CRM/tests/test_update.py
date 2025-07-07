import os
from pathlib import Path
from scripts import update


def test_stage_creates_accept(monkeypatch, tmp_path):
    test_dir = tmp_path / 'test'
    accept_dir = tmp_path / 'accept'
    called = []

    def fake_clone(repo, dest, branch="main"):
        dest.mkdir()
        (dest / 'f').write_text('x')

    def fake_run_tests(target):
        called.append('tests')
        return True

    monkeypatch.setattr(update, 'TEST_DIR', test_dir)
    monkeypatch.setattr(update, 'ACCEPT_DIR', accept_dir)
    monkeypatch.setattr(update, 'clone_or_update', fake_clone)
    monkeypatch.setattr(update, 'run_tests', fake_run_tests)

    update.stage('repo')
    assert (accept_dir / 'f').exists()
    assert 'tests' in called


def test_deploy_and_backup(monkeypatch, tmp_path):
    accept = tmp_path / 'accept'
    prod = tmp_path / 'prod'
    backups = tmp_path / 'backups'
    accept.mkdir()
    (accept / 'f').write_text('new')
    prod.mkdir()
    (prod / 'f').write_text('old')

    monkeypatch.setattr(update, 'ACCEPT_DIR', accept)
    monkeypatch.setattr(update, 'PROD_DIR', prod)
    monkeypatch.setattr(update, 'BACKUP_DIR', backups)
    monkeypatch.setattr(update, 'run', lambda *a, **k: None)

    update.deploy_to_production()

    assert (prod / 'f').read_text() == 'new'
    assert list(backups.glob('prod_*.tar.gz'))


def test_rollback(monkeypatch, tmp_path):
    prod = tmp_path / 'prod'
    backups = tmp_path / 'backups'
    prod.mkdir()
    (prod / 'file').write_text('one')

    monkeypatch.setattr(update, 'PROD_DIR', prod)
    monkeypatch.setattr(update, 'BACKUP_DIR', backups)
    monkeypatch.setattr(update, 'run', lambda *a, **k: None)

    update.backup_production()
    (prod / 'file').write_text('two')
    update.rollback()

    assert (prod / 'file').read_text() == 'one'
