import json
from unittest import mock
from scripts import asset_cli, config_cli, dmarc_cli, crm_sync_cli


def test_asset_cli_sync(monkeypatch, capsys):
    called = {}

    def fake_post(url, params, **kwargs):
        called['url'] = url
        called['params'] = params
        class Resp:
            def json(self_inner):
                return {'status': 'synced'}
        return Resp()
    monkeypatch.setattr(asset_cli, 'requests', mock.Mock(post=fake_post))
    asset_cli.sync(asset_cli.argparse.Namespace(source='all'))
    assert called['url'].endswith('/assets/sync')
    assert called['params'] == {'source': 'all'}


def test_config_cli_set(monkeypatch, capsys):
    called = {}

    def fake_post(url, params, **kwargs):
        called['url'] = url
        called['params'] = params
        class Resp:
            def json(self_inner):
                return {'model': params['model']}
        return Resp()
    monkeypatch.setattr(config_cli, 'requests', mock.Mock(post=fake_post))
    config_cli.set_api(config_cli.argparse.Namespace(key='k', model='gpt-4'))
    assert called['url'].endswith('/config/api')
    assert called['params'] == {'api_key': 'k', 'model': 'gpt-4'}


def test_dmarc_cli_report(monkeypatch):
    called = {}

    def fake_get(url, **kwargs):
        called['url'] = url

        class Resp:
            def json(self_inner):
                return {'domain': 'example.com', 'pass': 1, 'fail': 0}

        return Resp()

    monkeypatch.setattr(dmarc_cli, 'requests', mock.Mock(get=fake_get))
    dmarc_cli.report(dmarc_cli.argparse.Namespace(domain='example.com'))
    assert called['url'].endswith('/dmarc/example.com')


def test_dmarc_cli_crm_report(monkeypatch):
    called = {}

    def fake_get(url, **kwargs):
        called['url'] = url

        class Resp:
            text = 'ok'

        return Resp()

    monkeypatch.setattr(dmarc_cli, 'requests', mock.Mock(get=fake_get))
    dmarc_cli.crm_report(dmarc_cli.argparse.Namespace(tenant_id=1, domain='example.com', format='csv'))
    assert called['url'].endswith('/api/crm/dmarc/1/example.com?format=csv')


def test_dmarc_cli_add_domain(monkeypatch):
    called = {}

    def fake_post(url, params, **kwargs):
        called['url'] = url
        called['params'] = params

        class Resp:
            def json(self_inner):
                return {'id': 1}

        return Resp()

    monkeypatch.setattr(dmarc_cli, 'requests', mock.Mock(post=fake_post))
    dmarc_cli.add_domain(dmarc_cli.argparse.Namespace(tenant_id=2, domain='ex.com'))
    assert called['url'].endswith('/api/crm/domains/')
    assert called['params']['tenant_id'] == 2


def test_dmarc_cli_abuse(monkeypatch):
    called = {}

    def fake_post(url, params, **kwargs):
        called['url'] = url
        called['params'] = params

        class Resp:
            def json(self_inner):
                return {'status': 'sent'}

        return Resp()

    monkeypatch.setattr(dmarc_cli, 'requests', mock.Mock(post=fake_post))
    dmarc_cli.abuse(
        dmarc_cli.argparse.Namespace(
            tenant_id=3,
            domain='ex.com',
            ip='1.2.3.4',
            contact='owner'
        )
    )
    assert called['url'].endswith('/api/crm/dmarc/abuse')
    assert called['params']['ip'] == '1.2.3.4'


def test_dmarc_cli_abuse_status(monkeypatch):
    called = {}

    def fake_put(url, params, **kwargs):
        called['url'] = url
        called['params'] = params

        class Resp:
            def json(self_inner):
                return {'id': 1, 'status': params['status']}

        return Resp()

    monkeypatch.setattr(dmarc_cli, 'requests', mock.Mock(put=fake_put))
    dmarc_cli.abuse_status(dmarc_cli.argparse.Namespace(id=1, status='responded'))
    assert called['url'].endswith('/api/crm/dmarc/abuse/1')
    assert called['params']['status'] == 'responded'

def test_crm_sync_cli_import(monkeypatch):
    called = {}

    def fake_post(url, params, **kwargs):
        called['url'] = url
        called['params'] = params

        class Resp:
            def json(self_inner):
                return {'imported': 1}

        return Resp()

    monkeypatch.setattr(crm_sync_cli, 'requests', mock.Mock(post=fake_post))
    crm_sync_cli.import_sync(crm_sync_cli.argparse.Namespace(url='http://api'))
    assert called['url'].endswith('/api/crm/sync/import')
