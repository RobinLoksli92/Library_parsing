import argparse
from requests.models import HTTPError
import os
from pathlib import Path
import requests
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup
import lxml

from download import download_comments, download_image, download_txt


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def parse_book_page(soup):
    some_book = {}
    title_tag = soup.find('h1')
    title_text = title_tag.text
    splitted_title_text = title_text.split('::')
    book_title = splitted_title_text[0].strip()
    book_author = splitted_title_text[-1].strip()
    book_image = soup.find(class_='bookimage').find('img')['src']
    image_url = urljoin('https://tululu.org/', book_image)
    books_genres = soup.find_all('span', class_='d_book')
    book_genre = parse_book_genres(books_genres)
    book_comments = soup.find_all(class_='texts')
    comments = []
    for comment in book_comments:
        comment_text = comment.find(class_='black').text
        comments.append(comment_text)
         
    some_book['Заголовок'] = book_title
    some_book['Автор'] = book_author
    some_book['Жанр книги'] = book_genre
    some_book['Картинка'] = image_url
    some_book['Комменты'] = comments

    return some_book
    

def parse_book_genres(books_genres):
    for genre in books_genres:
            book_genres = genre.find('a')['title']
            book_genres = book_genres.split('-')
            book_genres = book_genres[0].split(',')
            return book_genres


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_id',default=1, type=int)
    parser.add_argument('--end_id', default=11, type=int)
    args = parser.parse_args()
    start_book_id = args.start_id
    end_book_id = args.end_id

    Path('books/').mkdir(parents=True, exist_ok=True)
    Path('images/').mkdir(parents=True, exist_ok=True)
    Path('comments/').mkdir(parents=True, exist_ok=True)

    for book_id in range(start_book_id, end_book_id):
        books_url = f'https://tululu.org/b{book_id}'
        books_response = requests.get(books_url)
        books_response.raise_for_status
        soup = BeautifulSoup(books_response.text, 'lxml')
        
        download_books_url = f'https://tululu.org/txt.php?id={book_id}'
        download_books_response = requests.get(download_books_url)
        download_books_response.raise_for_status

        try:
            check_for_redirect(download_books_response)
            some_book = parse_book_page(soup)
            book_title = some_book['Заголовок']
            # filename = f'{book_id}. {book_title}.txt'
            image_url = some_book['Картинка']
            image_url_path = urlsplit(image_url).path
            image_name = os.path.split(image_url_path)[-1]
            download_txt(download_books_response, filename=book_title)
            download_image(image_url, filename=image_name)
            download_comments(soup, filename=book_title)

        except requests.HTTPError:
            pass


if __name__ == '__main__':
    main()