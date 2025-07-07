from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def create_user_with_role(username: str, role: str):
    u_resp = client.post('/users/', params={'username': username, 'password': 'pw'})
    user_id = u_resp.json()['id']
    r_resp = client.post('/roles/', params={'name': role})
    role_id = r_resp.json()['id']
    client.post(f'/roles/{role_id}/assign/{user_id}')
    return user_id


def test_send_and_list_edi_message():
    dist_id = create_user_with_role('dist', 'distributor')
    admin_id = create_user_with_role('adm', 'admin')

    send_resp = client.post(
        '/edi/',
        json={
            'sender_type': 'distributor',
            'sender_id': 1,
            'receiver_type': 'partner',
            'receiver_id': 2,
            'content': 'order',
        },
        auth=('dist', 'pw'),
    )
    assert send_resp.status_code == 200

    list_resp = client.get('/edi/', auth=('adm', 'pw'))
    assert list_resp.status_code == 200
    assert any(m['content'] == 'order' for m in list_resp.json())
