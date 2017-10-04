#
from selenium import webdriver
import json 
from base64 import b64encode
import requests
from os.path import join as pjoin

with open('config.json','r') as f:
    config = json.load(f)

enterprise_user = config['user_name']
user_password = config['user_password']
host_addr = config['host_addr']

def get_basic_jwt():
    auth_encoded = 'Basic ' + b64encode("{}:{}".format(enterprise_user, user_password).encode('utf-8')).decode('utf-8')

    auth_answ = requests.post("{}/auth".format(host_addr),headers={'Authorization': auth_encoded})

    return auth_answ.headers['Www-Authenticate']

if __name__ == "__main__":
    with open(pjoin("tests", "session_key"),'w') as f:
        f.write(get_basic_jwt())
