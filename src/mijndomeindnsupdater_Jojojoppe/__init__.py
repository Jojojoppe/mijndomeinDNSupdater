import argparse
import json
import requests
from .dnsupdater import MijnDomein

def main(args=None):
    # Command-line argument parser
    parser = argparse.ArgumentParser(description="Update MijnDomijn DNS entries.")
    parser.add_argument(
        "-c", "--config", metavar="file", type=str, default="config.json",
        help="Change default config file."
    )
    
    args = parser.parse_args(args)

    # Config
    cnf_file=args.config
    try:
        cnf_data=open(cnf_file)
    except IOError:
        print("Config file does not exists!");
        return
    cnf = json.load(cnf_data)
    cnf_data.close()

    md = MijnDomein(cnf['email'], cnf['password'])
    md.login()
    md.getDomainNameInfo()
    
    for domain in cnf['domains']:
        print("->", domain['name'])
        md.getDNSRecords(domain['name'])
        for update in domain['updates']:
            print("::", update['type'], update['subdomain'])
            if update['function'] == 'static':
                md.update(domain['name'], update['type'], update['subdomain'], update['value'])
            elif update['function'] == 'getip':
                ip = requests.get('https://api.ipify.org').content.decode('utf8')
                md.update(domain['name'], update['type'], update['subdomain'], ip)
            elif update['function'] == 'getip6':
                ip = requests.get('https://api6.ipify.org').content.decode('utf8')
                md.update(domain['name'], update['type'], update['subdomain'], ip)
            else:
                print('Unknown function type')
        print(md.domainNameInfo)
        md.updateDNSRecords(domain['name'])

    md.logout()