import argparse
import requests

API_URL = 'http://localhost:8000'


def request(args):
    resp = requests.post(
        f'{API_URL}/certificates/request',
        json={'hostnames': args.hostnames, 'email': args.email, 'staging': args.staging},
        timeout=10,
    )
    print(resp.json())


parser = argparse.ArgumentParser(description='ACME certificate utilities')
sub = parser.add_subparsers(dest='command')

req_cmd = sub.add_parser('request', help='Request certificates')
req_cmd.add_argument('email')
req_cmd.add_argument('hostnames', nargs='+')
req_cmd.add_argument('--staging', action='store_true')
req_cmd.set_defaults(func=request)


def main():
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
