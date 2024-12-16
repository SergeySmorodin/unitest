import unittest
from unittest.mock import patch, Mock
import requests
from create_folder import YandexDisk


class TestYandexDisk(unittest.TestCase):

    @patch('requests.get')
    @patch('requests.put')
    def test_create_folder_exists(self, mock_put, mock_get):
        # Вариант, когда папка уже существует
        mock_get.return_value = Mock(status_code=200)
        disk = YandexDisk(ya_token='YA_TOKEN')
        disk.create_folder('new_folder')

        mock_get.assert_called_once()
        mock_put.assert_not_called()

    @patch('requests.get')
    @patch('requests.put')
    def test_create_folder_does_not_exist(self, mock_put, mock_get):
        # Вариант, когда папка не существует
        mock_get.return_value = Mock(status_code=404)
        mock_put.return_value = Mock(status_code=201)

        disk = YandexDisk(ya_token='YA_TOKEN')
        disk.create_folder('new_folder')

        mock_get.assert_called_once()
        mock_put.assert_called_once()

    @patch('requests.get')
    @patch('requests.put')
    def test_create_folder_api_error(self, mock_put, mock_get):
        mock_get.return_value = Mock(status_code=503, text="Сервис временно недоступен")

        disk = YandexDisk(ya_token='YA_TOKEN')
        with self.assertRaises(requests.exceptions.HTTPError) as context:
            disk.create_folder('new_folder')

        self.assertEqual(context.exception.response.status_code, 503)
        mock_put.assert_not_called()
        mock_get.assert_called_once()


if __name__ == '__main__':
    unittest.main()
