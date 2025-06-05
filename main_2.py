import requests
import configparser
from pprint import pprint
from tqdm import tqdm
import json

class SaveToYD:
    def __init__(self, token):
        self.token = token
        self.lst_photo = []

    
    def create_folder(self, folder_name):
        #Создание папки на яндекс диске
        url_ya = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path' : f'{folder_name}'}
        headers = {"Authorization": f'OAuth {self.token}'}
        requests.put(url_ya, params = params, headers = headers)

    
    def folders_on_disk(self):
        #Получение списка папок диска
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        return_list = []
        params = {'path' : '/'}
        headers = {"Authorization": f'OAuth {self.token}'}
        resp = requests.get(url, params=params, headers=headers)
        for elems in resp.json()['_embedded']['items']:
            return_list.append(elems['name'])
        return return_list


    def create_dogs_dict(self):
        #Создание списка пород собак, которые имеют подпороды
        url_breeds = 'https://dog.ceo/api/breeds/list/all'

        response_breeds = requests.get(url_breeds)
        breeds = response_breeds.json()['message']

        breeds_dict = {}
        for breed in breeds:
            if breeds[breed] == []:
                pass
            else:
                breeds_dict[breed] = breeds[breed]
        return breeds_dict


    def create_dogs_urls(self):
        #Создание словаря со ссылками на фотографии собак
        url_breeds = 'https://dog.ceo/api/breeds/list/all'

        response_breeds = requests.get(url_breeds)
        breeds = response_breeds.json()['message']

        breeds_list = []
        for breed in breeds:
            if breeds[breed] == []:
                breeds_list.append(breed)
            else:
                for elem in breeds[breed]:
                    breeds_list.append(f'{breed}-{elem}')    

        all_breeds_url = {}
        for breed in breeds_list:
            new_breed = breed.replace('-', '/') 
            all_breeds_url[breed] = f'https://dog.ceo/api/breed/{new_breed}/images'
        
        return all_breeds_url
    

    def load_photos(self, breed):
    #Метод который загружает на диск фотографии одной породы, или по 1 случайному фото каждой под-породы
        if breed in self.folders_on_disk():
            print('Фотографии этой породы уже есть на диске')
        else:
            dogs_dict = self.create_dogs_dict()
            self.create_folder(breed)
            if breed not in dogs_dict:
                resp = requests.get(dsk.create_dogs_urls()[breed])
                for url_photo in tqdm(resp.json()['message']):
                    path_write = f"{url_photo.split('/')[-2]}_{url_photo.split('/')[-1]}"
                    url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
                    params = {
                        'url': url_photo,
                        'path': f'{breed}/{path_write}'
                    }
                    headers = {"Authorization": f'OAuth {self.token}'}
                    requests.post(url, params=params, headers=headers)
                    self.lst_photo.append({breed : f"{url_photo.split('/')[-2]}_{url_photo.split('/')[-1]}"})
                    
            else:
                for subbreed in tqdm(dogs_dict[breed]):
                    sub_breed = f'{breed}-{subbreed}'   
                    resp = requests.get(f'{dsk.create_dogs_urls()[sub_breed]}/random')
                    path_write = f"{resp.json()['message'].split('/')[-2]}_{resp.json()['message'].split('/')[-1]}"
                    url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
                    params = {
                        'url': resp.json()['message'],
                        'path': f'{breed}/{path_write}'
                    }
                    headers = {"Authorization": f'OAuth {self.token}'}
                    requests.post(url, params=params, headers=headers)
                    self.lst_photo.append({breed : f"{resp.json()['message'].split('/')[-2]}_{resp.json()['message'].split('/')[-1]}"})
        with open('info_downloads.json', 'w', encoding='utf-8') as f:
            json.dump(self.lst_photo, f, ensure_ascii=False, indent=4, sort_keys=True) 


config = configparser.ConfigParser()
config.read('config.ini', encoding = 'utf-8')
TOKEN = config['token']['token']

dsk = SaveToYD(TOKEN)
dsk.load_photos('hound')
dsk.load_photos('boxer')
