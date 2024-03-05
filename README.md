# MijnDomein DNS updater
A python script using selenium and geckodriver to update the DNS records ad mijndomein.nl

## Installing
Currently this package cannot be found in the pypi repo's so installing should be done by cloning the repo and running
``` bash
pip install .
```

## Configuration
The mijndomein DNS updater uses a JSON file as configuration:
``` JSON
{
    "email": "<user email>",
    "password": "<user password>",
    "domains": [
        {
            "name": "<domain name>",
            "updates": [
                {
                    "type": "<A/AAA/CNAME/MX/TXT>",
                    "subdomain": "<subdomain.domain>",
                    "function": "<static/getip>",
                    "value": "<static value>"
                }
            ]
        }
    ]
}
```

## Usage
Run `dnsupdater` in the directory where a `config.json` can be found or provide the path to a config file with the `-c` or `--config` option

## Licence
This package is MIT licenced and the licence text can be found in `LICENCE`