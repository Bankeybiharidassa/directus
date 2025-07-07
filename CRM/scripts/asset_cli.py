#!/usr/bin/env python3
import argparse
import requests

API_URL = 'http://localhost:8000'


def sync(args):
    resp = requests.post(
        f'{API_URL}/assets/sync', params={'source': args.source}, timeout=10
    )
    print(resp.json())


parser = argparse.ArgumentParser(description='Manage assets')
sub = parser.add_subparsers(dest='command')

sync_cmd = sub.add_parser('sync', help='Sync assets from external sources')
sync_cmd.add_argument('--source', default='all')
sync_cmd.set_defaults(func=sync)


def main():
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
