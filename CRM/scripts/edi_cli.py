#!/usr/bin/env python3
import argparse
import requests

API_URL = 'http://localhost:8000'


def send(args):
    params = {
        'sender_type': args.sender_type,
        'sender_id': args.sender_id,
        'receiver_type': args.receiver_type,
        'receiver_id': args.receiver_id,
        'content': args.content,
    }
    auth = (args.username, args.password)
    resp = requests.post(
        f'{API_URL}/edi/', params=params, auth=auth, timeout=10
    )
    print(resp.json())


parser = argparse.ArgumentParser(description='Manage EDI messages')
sub = parser.add_subparsers(dest='command')

send_cmd = sub.add_parser('send', help='Send EDI message')
send_cmd.add_argument('--sender-type', required=True)
send_cmd.add_argument('--sender-id', type=int, required=True)
send_cmd.add_argument('--receiver-type', required=True)
send_cmd.add_argument('--receiver-id', type=int, required=True)
send_cmd.add_argument('--content', required=True)
send_cmd.add_argument('--username', required=True)
send_cmd.add_argument('--password', required=True)
send_cmd.set_defaults(func=send)


def main():
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
