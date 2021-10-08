![GitHub Workflow Status](https://img.shields.io/github/workflow/status/igroykt/letsencrypt-godaddy/letsencrypt-godaddy%20build)
![GitHub](https://img.shields.io/github/license/igroykt/letsencrypt-godaddy)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/igroykt/letsencrypt-godaddy)

# LetsEncrypt GoDaddy
Application to obtain wildcard certificates with DNS challenge using GoDaddy DNS API.

## Dependencies
* Python 3.6+
* Certbot

## Unix
### Build and install 
```
pip3 install certbot
pip3 install -r requirements.txt
mv config.sample.ini config.ini
# setup config.ini
python setup.py build
mkdir $HOME/letsencrypt-godaddy
mv build/* $HOME/letsencrypt-godaddy
mv config.ini $HOME/letsencrypt-godaddy
$HOME/letsencrypt-godaddy/main -a
```
Encryption key change on every build.

### Setup
About APIKEY and APISECRET read here https://developer.godaddy.com/getstarted.

Run "./main -a" to input API authentication data.

Info about configuration options read on wiki.

### Confidentiality
You must safely keep API authentication data for security reason. That is why Python scripts compile into binary and authentication data keep encrypted.

### Examples
First run:
```
$HOME/main -v -n
```
Test run:
```
$HOME/main -v -t
```
Renew certificates:
```
$HOME/main -v
```

### Clean of TXT
Godaddy API by default removes all TXT records that match "_acme-challenge". So don't worry about junk.

### Cron
```
#m      #h      #dom    #mon    #dow    #command
0 	    0 	    1 	    * 	    * 	    /path/to/letsencrypt-godaddy/main
```

## Windows
### Build and install
```
# install certbot https://dl.eff.org/certbot-beta-installer-win32.exe
pip install -r requirements.txt
move config.sample.ini config.ini
# setup config.ini
python setup.py build
mkdir c:\letsencrypt-godaddy
move build\* c:\letsencrypt-godaddy
move config.ini c:\letsencrypt-godaddy
c:\letsencrypt-godaddy\main.exe -a
```