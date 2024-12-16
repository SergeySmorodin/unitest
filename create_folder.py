import requests
import os
from dotenv import load_dotenv

load_dotenv()


class YandexDisk:

    def __init__(self, ya_token):
        self.YA_TOKEN = ya_token

    def create_folder(self, folder_name):
        url = f"https://cloud-api.yandex.net/v1/disk/resources"
        headers = {
            'Authorization': f'OAuth {self.YA_TOKEN}'
        }
        params = {
            "path": folder_name
        }

        # Проверяем, существует ли папка
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            print(f"Папка '{folder_name}' уже существует.")
            return
        elif response.status_code == 404:
            response = requests.put(url, headers=headers, params=params)
            response.raise_for_status()
            print(f"Папка '{folder_name}' успешно создана.")
        else:
            print(f"Ошибка создания папки: {response.status_code} - {response.text}")
            raise requests.exceptions.HTTPError(response=response)


if __name__ == '__main__':
    YA_TOKEN = os.getenv('YA_TOKEN')
    disk = YandexDisk(ya_token=YA_TOKEN)

    folder_name = "test_folder"
    disk.create_folder(folder_name)
