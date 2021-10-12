from urllib import parse
from requests.models import HTTPError
import os
from pathlib import Path
import requests
from urllib.parse import urljoin, urlsplit
from urllib.parse import urlparse
from pathvalidate import sanitize_filename

from bs4 import BeautifulSoup


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(response, filename, folder ='books/'): 
    sanitazed_filename = sanitize_filename(filename)
    filepath = os.path.join(folder, sanitazed_filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def download_image(image_url, filename, folder='images/'):
    response = requests.get(image_url)
    response.raise_for_status
    sanitazed_filename = sanitize_filename(filename)
    filepath = os.path.join(folder, sanitazed_filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


books_path = 'books/'
Path(books_path).mkdir(parents=True, exist_ok=True)
images_path = 'images/'
Path(images_path).mkdir(parents=True, exist_ok=True)

for book_id in range(1,11):
    books_url = f'https://tululu.org/b{book_id}'
    books_response = requests.get(books_url)
    books_response.raise_for_status
    soup = BeautifulSoup(books_response.text, 'lxml')
    title_tag = soup.find('h1')
    title_text = title_tag.text
    splitted_title_text = title_text.split('::')
    book_title = splitted_title_text[0].strip()
    
    download_books_url = f'https://tululu.org/txt.php?id={book_id}'
    download_books_response = requests.get(download_books_url)
    download_books_response.raise_for_status

    try:
        check_for_redirect(download_books_response)
        filename = f'{book_id}. {book_title}.txt'
        # download_txt(download_books_response, filename)
        book_image = soup.find(class_='bookimage').find('img')['src']
        image_url = urljoin('https://tululu.org/', book_image)
        image_name = book_image.split('/')[-1]
        download_image(image_url, filename=image_name)

    except requests.HTTPError:
        pass
    
    
