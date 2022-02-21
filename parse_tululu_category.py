import argparse
import json
import os
import requests
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
import lxml

from check_for_redirect import check_for_redirect
from download import download_image, download_txt
from book_page_parser import parse_book_page


book_discription = []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_page',default=1, type=int)
    parser.add_argument('--end_page', default=701, type=int)  
    parser.add_argument('--dest_img_folder', default='images/', type=str)
    parser.add_argument('--dest_txt_folder', default='books', type=str)
    parser.add_argument('--json_path', default='', type=str)
    parser.add_argument('--skip_imgs', default=True, action='store_false')
    parser.add_argument('--skip_txt', default=True, action='store_false')
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
                if args.skip_imgs and args.skip_txt:
                    download_txt(book_id, filename=book_title, folder = args.dest_txt_folder)
                    download_image(image_url, book_id, filename=image_name, folder=args.dest_img_folder)
                elif not args.skip_imgs:
                    download_txt(book_id, filename=book_title, folder = args.dest_txt_folder)
                elif not args.skip_txt:
                    download_image(image_url, book_id, filename=image_name, folder=args.dest_img_folder)
                elif not args.skip_imgs and not args.skip_txt:
                    pass
            except requests.HTTPError:
                pass
    with open(f'{args.json_path}book_discription.json','w', encoding='utf-8') as file:
        json.dump(book_discription, file, ensure_ascii=False)


if __name__ == '__main__':
    main()
