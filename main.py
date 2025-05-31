import requests
import configparser
from pprint import pprint
from tqdm import tqdm
import json


class SavePicture:
    def __init__(self, token):
        self.token = token
        self.dict_photo = {}
    

    def create_folder(self, folder_name):
        url_ya = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path' : f'{folder_name}'}
        headers = {"Authorization": f'OAuth {self.token}'}
        requests.put(url_ya, params = params, headers = headers)


    def create_dogs_dict(self):
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
    

    def photos_one_breed(self, breed_dog, folder_name):
        if breed_dog not in self.create_dogs_dict():
            url_photos_breed = self.create_dogs_urls()[breed_dog]
            breed_photo = requests.get(url_photos_breed)
            photo_url = breed_photo.json()['message']
            for elem in tqdm(photo_url):
                photo_dog_url = requests.get(elem)
    
                url_for_get_downloads = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
                path_write = f'{elem.split('/')[-2]}.{elem.split('/')[-1]}'
                params_write_file = {'path' : f'{folder_name}/{path_write}'}
                headers_write = {'Authorization': f'OAuth {self.token}'}
                url_for_downloads = requests.get(url_for_get_downloads, params = params_write_file, headers = headers_write)
                resp = requests.put(f'{url_for_downloads.json()['href']}', data = photo_dog_url)
                if self.dict_photo.get(elem.split('/')[-2]) == None:
                    self.dict_photo[elem.split('/')[-2]] = [elem.split('/')[-1]]
                else:
                    self.dict_photo[elem.split('/')[-2]].append(elem.split('/')[-1])
                with open('info_downloads.json', 'w', encoding='utf-8') as f:
                    json.dump(self.dict_photo, f, ensure_ascii=False, indent=4, sort_keys=True)
        else:
            for elems in tqdm(self.create_dogs_dict()[breed_dog]):
                sub_breed = f'{breed_dog}-{elems}'
                url_photos_breed = f'{self.create_dogs_urls()[sub_breed]}/random'
                breed_photo = requests.get(url_photos_breed)
                photo_url = breed_photo.json()['message']
                photo_dog_url = requests.get(photo_url)

                url_for_get_downloads = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
                path_write = f'{photo_url.split('/')[-2]}.{photo_url.split('/')[-1]}'  
                params_write_file = {'path': f'{folder_name}/{path_write}'}
                headers_write = {'Authorization': f'OAuth {self.token}'}
                url_for_downloads = requests.get(url_for_get_downloads, params = params_write_file, headers = headers_write)
                resp = requests.put(url_for_downloads.json()['href'], data = photo_dog_url)
                if self.dict_photo.get(photo_url.split('/')[-2]) == None:  
                    self.dict_photo[photo_url.split('/')[-2]] = [photo_url.split('/')[-1]]
                else:
                    self.dict_photo[photo_url.split('/')[-2]].append(photo_url.split('/')[-1])
                with open('info_downloads.json', 'w', encoding='utf-8') as f:
                    json.dump(self.dict_photo, f, ensure_ascii=False, indent=4, sort_keys=True)
    
                          
            



config = configparser.ConfigParser()
config.read('config.ini', encoding = 'utf-8')
TOKEN = config['token']['token']


dogs = SavePicture(TOKEN)
dogs.create_folder('h')
dogs.photos_one_breed('hound', 'h')


