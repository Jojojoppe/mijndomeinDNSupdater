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
Furthermore a webdriver is needed like Chromedriver, Firefox and PhantomJS. Since this is differently on many distributions and sometimes even impossible on some machines (like raspberry pi: only Firefox works), you need to figure out yourself how to install that!

When running on a headless machine, `pyvirtualdisplay` is needed. Furtunately this is simply installed using pip:
```
sudo pip3 install pyvirtualdisplay
```

## Configuration
The mijndomein DNS updater uses a JSON file as configuration. In that file the user email and password must be provided. For each domain the user wants to update the DNS recods the corresponding subdomains must be mentioned. Furthermore the using webdriver can be selected with the `driver` tag. One can choose between `chrome`, `firefox`, and `phantomjs`. Currently Chromedriver and PhantomJS work.
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
	],
	"driver":"<a driver>",
	"display":<boolean: display?>
}

```

## Usage
Just run `./main` to run the updater with the standard configuration file `config.cnf`. If another configuration file is wanted, this can be done using `./main -c path/to/file` or `./main --config path/to/file`.
This information is also given with `./main -help` of `./main --help`.

## NOTE
Build pass testing is not yet done for the Firefox and PhantomJS webdrivers!
