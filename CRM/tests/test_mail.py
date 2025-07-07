from fastapi.testclient import TestClient
from backend.main import app
import os

client = TestClient(app)


def test_mail_sync_and_list(monkeypatch):
    class FakeConn:
        def login(self, user, pw):
            pass

        def select(self, mailbox):
            pass

        def search(self, charset, criterion):
            return "OK", [b"1 2"]

        def fetch(self, msg_id, _):
            messages = {
                b"1": (b"1", b"Subject: Hello\r\nFrom: a@example.com\r\nMessage-ID: <m1>\r\nDate: Mon, 1 Jan 2024 10:00:00 +0000\r\n\r\n"),
                b"2": (b"2", b"Subject: Hi\r\nFrom: b@example.com\r\nMessage-ID: <m2>\r\nDate: Tue, 2 Jan 2024 10:00:00 +0000\r\n\r\n"),
            }
            return "OK", [messages[msg_id]]

        def logout(self):
            pass

    def fake_imap(host):
        return FakeConn()

    monkeypatch.setattr("backend.routes.mail.imaplib.IMAP4_SSL", fake_imap)
    os.environ["IMAP_HOST"] = "imap.test"
    os.environ["IMAP_USER"] = "user"
    os.environ["IMAP_PASSWORD"] = "pw"

    sync_resp = client.post("/mail/sync")
    assert sync_resp.status_code == 200
    assert sync_resp.json()["new_messages"] == 2

    list_resp = client.get("/mail/messages")
    assert list_resp.status_code == 200
    data = list_resp.json()
    assert len(data) == 2
