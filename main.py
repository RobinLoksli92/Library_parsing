from pathlib import Path
import requests

from bs4 import BeautifulSoup

from requests.models import HTTPError

from bs4_tutorial import download_txt

def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


books_path = 'books/'
Path(books_path).mkdir(parents=True, exist_ok=True)


for book_id in range(1,11):
    books_url = f'https://tululu.org/b{book_id}'
    books_response = requests.get(books_url)
    books_response.raise_for_status
    soup = BeautifulSoup(books_response.text, 'lxml')
    title_tag = soup.find('h1')
    title_text = title_tag.text
    splitted_title_text = title_text.split('::')
    title = splitted_title_text[0].strip()

    download_books_url = f'https://tululu.org/txt.php?id={book_id}'
    download_books_response = requests.get(download_books_url)
    download_books_response.raise_for_status

    # try:
    #     check_for_redirect(download_books_response)
    #     filename = f'{book_id}. {title}.txt'
    #     filepath = download_txt(download_books_url, filename)
        
    #     with open(filepath, 'wb') as file:
    #         file.write(download_books_response.content)       
    # except requests.HTTPError:
    #     pass
    
    
