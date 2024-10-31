import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload() -> None:
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open("books.json", "r") as my_file:
        books_json = my_file.read()

    books = list(
        chunked(chunked(json.loads(books_json), 2), 20)
    )

    os.makedirs('pages', exist_ok=True)

    for i, book_page in enumerate(books, 1):
        print(book_page)
        rendered_page = template.render(
            books=book_page
        )

        with open(os.path.join('pages', f'index{i}.html'), 'w', encoding="utf8") as file:
            file.write(rendered_page)


on_reload()

server = Server()

server.watch('template.html', on_reload)

server.serve(root='.')
