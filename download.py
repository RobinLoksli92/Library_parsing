import os
from pathvalidate import sanitize_filename
import requests

from check_for_redirect import check_for_redirect


def download_txt(book_id, filename, folder ='books/'): 
    download_books_url = f'https://tululu.org/txt.php'
    payload = {
        'id': book_id
    } 
    download_books_response = requests.get(download_books_url, params=payload)
    download_books_response.raise_for_status()
    check_for_redirect(download_books_response)
    sanitazed_filename = sanitize_filename(filename)
    filepath = os.path.join(folder, sanitazed_filename)
    with open(f'{filepath}_{book_id}.txt', 'wb') as file:
        file.write(download_books_response.text)
    return filepath


def download_image(image_url, book_id, filename, folder='images/'):
    response = requests.get(image_url)
    response.raise_for_status()
    sanitazed_filename = sanitize_filename(filename)
    filepath = f'{folder}{book_id}_{sanitazed_filename}'
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath