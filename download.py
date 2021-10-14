import os
from pathvalidate import sanitize_filename
import requests


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


def download_comments(soup, filename, folder='comments/'):
    filepath = f'{folder}{filename}.txt'
    book_comments = soup.find_all(class_='texts')
    with open(filepath, 'wb') as file:
        for comment in book_comments:
            comment_text = comment.find(class_='black').text
            file.write(comment_text.encode())