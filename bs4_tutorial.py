import os
import  requests
from pathvalidate import sanitize_filename

from bs4 import BeautifulSoup
import lxml


def download_txt(url, filename, folder ='books/'):
    sanitazed_filename = sanitize_filename(filename)
    filepath = os.path.join(folder, sanitazed_filename)
    return filepath
  


url = 'https://tululu.org/b1/'

response = requests.get(url)
response.raise_for_status

soup = BeautifulSoup(response.text, 'lxml')
title_tag =soup.find('h1')
title_text = title_tag.text
splitted_title_text = title_text.split('::')
title = splitted_title_text[0]
author = splitted_title_text[1].strip()
filepath = download_txt(url=url, filename='Али/\\би', folder = 'txt/' )
# print(filepath)