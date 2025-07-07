#!/usr/bin/env python3
import argparse
import requests

API_URL = 'http://localhost:8000'


def set_api(args):
    resp = requests.post(
        f'{API_URL}/config/api',
        params={'api_key': args.key, 'model': args.model},
        timeout=10,
    )
    print(resp.json())


def get_api(_args):
    resp = requests.get(f'{API_URL}/config/api', timeout=10)
    print(resp.json())


def list_models(_args):
    resp = requests.get(f'{API_URL}/config/models', timeout=10)
    print(resp.json())


parser = argparse.ArgumentParser(description='Manage API configuration')
sub = parser.add_subparsers(dest='command')

set_cmd = sub.add_parser('set-api', help='Set API key and model')
set_cmd.add_argument('--key', required=True)
set_cmd.add_argument('--model', required=True)
set_cmd.set_defaults(func=set_api)

sub.add_parser('get-api', help='Show API config').set_defaults(func=get_api)
sub.add_parser('list-models', help='List models').set_defaults(func=list_models)


def main():
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
