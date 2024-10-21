import json
from pprint import pprint

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
        chunked(json.loads(books_json), 2)
    )
    rendered_page = template.render(
        books=books
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


on_reload()

server = Server()

server.watch('template.html', on_reload)

server.serve(root='.')
