# Check HTTPS Validation

This script checks validity of HTTPS certificate.

# How it works

Input parameter is path to file which contains https urls like:
```
https://mail.ru
https://devman.org
https://something-else.com
```
Delimiter is '\n'.

Script reads this file and transform data to list. After that script tries to get every url data in list asynchronously with ssl verification.
If verification succeeded, url writes to file with name 'Valid' in current directory, otherwise 'Unvalid'.

Script is written for python3.6.

# How to run on linux:
1. Clone repo
```
$ git clone https://github.com/paganism/check_https_validation
```
2. Create virtual environment in repo directory
```
$ virtualenv -p /usr/bin/python3.6 .venv
```
3. Activate virtual environment
```
$ source .venv/bin/activate
```
4. Install requirements
```
$ pip install -r requirements.txt
```
5. Run script
```
$ python3.6 https_validation.py --path /home/user/hosts.txt
```
After that in project directory you will see 2 output files: 'Valid' and 'Unvalid'.
Don't forget to create hosts.txt or modify file from repository.

# Project Goals

The code is written for educational purposes.
