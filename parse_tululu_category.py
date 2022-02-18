import argparse
import json
import os
from pprint import pprint
import requests
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup
import lxml

from check_for_redirect import check_for_redirect
from download import download_image, download_txt
from main import parse_book_page


book_discription = []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_page',default=1, type=int)
    parser.add_argument('--end_page', default=701, type=int)
    args = parser.parse_args()

    with open('book_discription.json','r', encoding='utf-8') as file:
        for book in json.load(file):
            book_discription.append(book)

    for page in range(args.start_page, args.end_page):
        url = f'http://tululu.org/l55/{page}'
        response = requests.get(url)
        response.raise_for_status()
        fantastic_books = response.text
        soup = BeautifulSoup(fantastic_books, 'lxml')
        imagelink_selector = '.d_book a[href*="/b"]'
        books_links = soup.select(imagelink_selector)
        for book_link in books_links:
            book_link = book_link['href']
            book_url = f'http://tululu.org{book_link}'
            try:
                book_response = requests.get(book_url)
                book_response.raise_for_status()
                check_for_redirect(book_response)
                soup = BeautifulSoup(book_response.text, 'lxml')
                some_book = parse_book_page(soup)
                book_discription.append(some_book)
                book_title = some_book['Заголовок']
                image_url = some_book['Картинка']
                image_url_path = urlsplit(image_url).path
                image_name = os.path.split(image_url_path)[-1]
                book_id = ''.join([symbol for symbol in book_link if symbol.isdigit()])
                download_txt(book_id, filename=book_title)
                download_image(image_url, book_id, filename=image_name)
            except requests.HTTPError:
                pass
    with open('book_discription.json','w', encoding='utf-8') as file:
        json.dump(book_discription, file, ensure_ascii=False)


if __name__ == '__main__':
    main()
