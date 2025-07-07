#!/usr/bin/env python3
import argparse
import requests

API_URL = 'http://localhost:8000'


def import_sync(args):
    resp = requests.post(
        f'{API_URL}/api/crm/sync/import', params={'source_url': args.url}, timeout=10
    )
    print(resp.json())


parser = argparse.ArgumentParser(description='CRM sync utilities')
sub = parser.add_subparsers(dest='command')

imp_cmd = sub.add_parser('import', help='Import tenants and users')
imp_cmd.add_argument('--url')
imp_cmd.set_defaults(func=import_sync)


def main():
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
