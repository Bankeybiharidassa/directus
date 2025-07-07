#!/usr/bin/env python3
import argparse
import requests

API_URL = 'http://localhost:8000'


def report(args):
    resp = requests.get(f'{API_URL}/dmarc/{args.domain}', timeout=10)
    print(resp.json())


def crm_report(args):
    url = f"{API_URL}/api/crm/dmarc/{args.tenant_id}/{args.domain}?format={args.format}"
    resp = requests.get(url, timeout=10)
    print(resp.text)


def add_domain(args):
    url = f"{API_URL}/api/crm/domains/"
    params = {
        "tenant_id": args.tenant_id,
        "domain": args.domain,
    }
    resp = requests.post(url, params=params, timeout=10)
    print(resp.json())


def abuse(args):
    url = f"{API_URL}/api/crm/dmarc/abuse"
    params = {
        "tenant_id": args.tenant_id,
        "domain": args.domain,
        "ip": args.ip,
        "contact": args.contact,
    }
    resp = requests.post(url, params=params, timeout=10)
    print(resp.json())


def abuse_status(args):
    url = f"{API_URL}/api/crm/dmarc/abuse/{args.id}"
    resp = requests.put(url, params={"status": args.status}, timeout=10)
    print(resp.json())


parser = argparse.ArgumentParser(description='DMARC utilities')
sub = parser.add_subparsers(dest='command')

report_cmd = sub.add_parser('report', help='Get DMARC report for domain')
report_cmd.add_argument('domain')
report_cmd.set_defaults(func=report)

crm_cmd = sub.add_parser('crm-report', help='Get CRM DMARC stats')
crm_cmd.add_argument('tenant_id', type=int)
crm_cmd.add_argument('domain')
crm_cmd.add_argument('--format', default='json')
crm_cmd.set_defaults(func=crm_report)

domain_cmd = sub.add_parser('add-domain', help='Add domain to tenant')
domain_cmd.add_argument('tenant_id', type=int)
domain_cmd.add_argument('domain')
domain_cmd.set_defaults(func=add_domain)

abuse_cmd = sub.add_parser('abuse', help='Report abuse')
abuse_cmd.add_argument('tenant_id', type=int)
abuse_cmd.add_argument('domain')
abuse_cmd.add_argument('ip')
abuse_cmd.add_argument('contact')
abuse_cmd.set_defaults(func=abuse)

status_cmd = sub.add_parser('abuse-status', help='Update abuse status')
status_cmd.add_argument('id', type=int)
status_cmd.add_argument('status')
status_cmd.set_defaults(func=abuse_status)


def main():
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
