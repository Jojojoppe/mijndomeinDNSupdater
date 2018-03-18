# mijndomein DNS updater
![Travis](https://img.shields.io/travis/Jojojoppe/mijndomeinDNSupdater.svg)
![MIT Licence](https://img.shields.io/badge/license-MIT-blue.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)

A python script using selenium and chromedriver (from chromium) to update the DNS records at mijndomein.nl (currently only A records)

## Installing
Installing the mijndomein DNS updater is as simply as downloading the main python file with the config file and put it somewhere where you want. Selenium is needed. Installing selenium can be as easy as
```
sudo pip3 install selenium
```
Furthermore chromedriver is needed. Installing chromium-browser should be enough. If not, try to find it in the repositories of your distribution. On arch chromedriver is in the AUR:
```
yaourt -S chromedriver
```

## Configuration
The mijndomein DNS updater uses a JSON file as configuration. In that file the user email and password must be provided. For each domain the user wants to update the DNS recods the corresponding subdomains must be mentioned.
```
{
	"email":"<user email>",
	"password":"<user password>",
	"domains":[
		{
			"name":"<a domain>",
			"subdomains":[
				"<a subdomain>"
			]
		}
	]
}

```

## Usage
Just run `./main` to run the updater with the standard configuration file `config.cnf`. If another configuration file is wanted, this can be done using `./main -c path/to/file` or `./main --config path/to/file`.
This information is also given with `./main -help` of `./main --help`.
