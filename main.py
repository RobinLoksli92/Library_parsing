import argparse
from requests.models import HTTPError
import os
from pathlib import Path
import requests
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
import lxml

from book_page_parser import parse_book_page
from check_for_redirect import check_for_redirect
from download import download_image, download_txt
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_id',default=1, type=int)
    parser.add_argument('--end_id', default=11, type=int)
    args = parser.parse_args()
    
    Path('books/').mkdir(parents=True, exist_ok=True)
    Path('images/').mkdir(parents=True, exist_ok=True)

    for book_id in range(args.start_id, args.end_id):
        book_url = f'https://tululu.org/b{book_id}/' 
        try:
            book_response = requests.get(book_url)
            book_response.raise_for_status()
            check_for_redirect(book_response)
            soup = BeautifulSoup(book_response.text, 'lxml')
            some_book = parse_book_page(soup)
            book_title = some_book['Заголовок']
            image_url = some_book['Картинка']
            image_url_path = urlsplit(image_url).path
            image_name = os.path.split(image_url_path)[-1]
            download_txt(book_id, filename=book_title)
            download_image(image_url, book_id, filename=image_name)

        except requests.HTTPError:
            pass


if __name__ == '__main__':
    main()