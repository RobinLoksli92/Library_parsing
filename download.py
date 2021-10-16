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
    with open(f'{filepath}.txt', 'wb') as file:
        file.write(download_books_response.content)
    return filepath


def download_image(image_url, filename, folder='images/'):
    response = requests.get(image_url)
    response.raise_for_status()
    sanitazed_filename = sanitize_filename(filename)
    filepath = os.path.join(folder, sanitazed_filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def download_comments(soup, filename, folder='comments/'):
    filepath = f'{folder}{filename}.txt'
    book_comments = soup.find_all(class_='texts')
    with open(filepath, 'wb') as file:
        for comment in book_comments:
            comment_text = comment.find(class_='black').text
            file.write(comment_text.encode())