import requests
import configparser
from pprint import pprint
from tqdm import tqdm
import json


class SavePicture:
    def __init__(self, token):
        self.token = token
    
    def create_folder(self, folder_name):
        url_ya = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path' : f'{folder_name}'}
        headers = {"Authorization": f'OAuth {self.token}'}
        requests.put(url_ya, params = params, headers = headers)



config = configparser.ConfigParser()
config.read('config.ini', encoding = 'utf-8')
TOKEN = config['token']['token']


dogs = SavePicture(TOKEN)
dogs.create_folder('DOGS')