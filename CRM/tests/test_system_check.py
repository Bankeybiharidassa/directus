from scripts import system_check
import builtins


def test_system_check_run(monkeypatch):
    output = {}
    def fake_print(msg):
        output['msg'] = msg
    monkeypatch.setattr(builtins, 'print', fake_print)
    system_check.main()
    assert 'disk' in output['msg']
