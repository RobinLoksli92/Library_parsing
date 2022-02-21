from urllib.parse import urljoin


def parse_book_page(soup):
    title_text = soup.find('h1').text
    book_title, book_author = title_text.split('::')
    book_title = book_title.strip()
    book_author = book_title.strip()
    book_image = soup.find(class_='bookimage').find('img')['src']
    image_url = urljoin('https://tululu.org/', book_image)
    books_genres = soup.find('span', class_='d_book')
    book_genre = [genre.text for genre in books_genres.find_all('a')]
    book_comments = soup.find_all(class_='texts')
    comments = [comment.find(class_='black').text for comment in book_comments]
    some_book = {
        'Заголовок' : book_title,
        'Автор' : book_author,
        'Жанр' : book_genre,
        'Картинка' : image_url,
        'Комменты' : comments
    }
    return some_book