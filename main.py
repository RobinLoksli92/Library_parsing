import argparse
from posixpath import split
from requests.models import HTTPError
import os
from pathlib import Path
import requests
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup
import lxml

from check_for_redirect import check_for_redirect
from download import download_image, download_txt


def parse_book_page(soup):
    title_text = soup.find('h1').text
    book_title, book_author = title_text.split('::')
    book_title = book_title.strip()
    book_author = book_title.strip()
    book_image = soup.find(class_='bookimage').find('img')['src']
    image_url = urljoin('https://tululu.org/', book_image)
    books_genres = soup.find_all('span', class_='d_book')
    book_genre = parse_book_genres(books_genres)
    book_comments = soup.find_all(class_='texts')
    comments = [comment.find(class_='black').text for comment in book_comments]
    some_book = {
        'Заголовок' : book_title,
        'Автор' : book_author,
        'Жанр книги' : book_genre,
        'Картинка' : image_url,
        'Комменты' : comments
    }
    return some_book
    

def parse_book_genres(books_genres):
    book_genre = [genre.find('a')['title'].split('-')[0].split(',') for genre in books_genres]
    return book_genre


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_id',default=1, type=int)
    parser.add_argument('--end_id', default=11, type=int)
    args = parser.parse_args()
    
    Path('books/').mkdir(parents=True, exist_ok=True)
    Path('images/').mkdir(parents=True, exist_ok=True)
    Path('comments/').mkdir(parents=True, exist_ok=True)

    for book_id in range(args.start_id, args.end_id):
        book_url = f'https://tululu.org/b{book_id}/'
        
        book_response = requests.get(book_url)
        book_response.raise_for_status()

        try:
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
            print('Ошибочка вышла')


if __name__ == '__main__':
    main()