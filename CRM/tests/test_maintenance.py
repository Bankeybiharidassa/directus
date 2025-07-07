import os


def test_menu_options_exist():
    with open('maintenance.sh') as f:
        data = f.read()
    assert 'Please select an action:' in data
    assert 'Update base system' in data
    assert 'Run system hardening check' in data
    assert 'Pull latest project updates' in data
    assert 'Restart updated services' in data


def test_update_starts_with_apt_update():
    with open('maintenance.sh') as f:
        lines = f.read().splitlines()
    idx = lines.index('update_system() {')
    snippet = '\n'.join(lines[idx:idx+3])
    assert 'apt update' in snippet


def test_hardening_contains_sysctl():
    with open('maintenance.sh') as f:
        data = f.read()
    assert 'net.ipv4.ip_forward' in data
    assert '/var/log/maintenance.log' in data
    assert '/opt/nucleus-platform' in data
