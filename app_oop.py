import requests
import sys
import json
import argparse
import shelve
from typing import Dict, List


class Book:
    def __init__(self, title: str, author: str, genre: str, publicationYear: int, isbnIssn: int, id: int):
        self.title = title
        self.author = author
        self.genre = genre
        self.publicationYear = publicationYear
        self.isbnIssn = isbnIssn
        self.id = id

    @classmethod
    def create_book(cls, title: str, author: str, genre: str, publicationYear: int, isbnIssn: int, id: int) -> "Book":
        return cls(title, author, genre, publicationYear, isbnIssn, id)

    def show_book(self) -> str:
        return (f"""title: {self.title}
author: {self.author}
genre: {self.genre}
publicationYear: {self.publicationYear}
isbnIssn: {self.isbnIssn}
id: {self.id}""")

    def __str__(self) -> str:
        return self.show_book()

    def get_title(self) -> str:
        return self.title


class BookSearchEngine:
    def __init__(self, author: str, **kwargs: Dict):
        self.author = author
        self.kwargs = kwargs

    def lookup_for_books(self) -> List:
        books_list = []
        base_url = 'https://data.bn.org.pl/api/bibs.json?'
        url = base_url + f'author={self.author}'

        # build url with optional arguments
        for k, v in self.kwargs.items():
            url += f'&{k}={v}'

        try:
            result = requests.get(url)
            result.raise_for_status()
            result = json.loads(result.text)
            bibs = result['bibs']
            for book in bibs:
                title = book['title']
                author = book['author']
                genre = book['genre']
                publicationYear = book['publicationYear']
                isbnIssn = book['isbnIssn']
                id = book['id']
                books_list.append(Book(title, author, genre, publicationYear, isbnIssn, id))
            return books_list
        except requests.exceptions.ConnectionError as erce:
            print(f'Ups! Something goes wrong: \n {erce}')
            exit(1)

    def represent_books(self) -> None:
        books_list = self.lookup_for_books()
        for book in books_list:
            print(book)

    def add_to_shelve(self) -> None:
        shelf_file = shelve.open('my_library2')
        books_list = self.lookup_for_books()
        if not books_list:
            print('Ups! Book you are looking for do not exist. Did you provide correct author and id?')
        for book in books_list:
            shelf_file[book.get_title()] = book
            print(f'{book.get_title()} has been successfully added to your library file!')
            shelf_file.close()

    @staticmethod
    def show_library_content() -> None:
        shelf_file = shelve.open('my_library2')
        key_list = list(shelf_file.keys())
        for key in key_list:
            print(f'{shelf_file[key]}\n')

        books_count = len(key_list)
        print(f'Total amount of books in your library: {books_count}')


class ArgumentsParser:
    def __init__(self) -> None:
        usage = """
            app.py <action> ... 

        Possible actions:
        app.py search <author>               <- will search for books with specified author. 
        app.py show                          <- will show books in your local library file.
        app.py add <author> --id <id>        <- will add book identified by author and id to your local library file.


        Example:
            app.py search Sanderson,Brandon --title Elantris
            app.py search Herbert,Frank --title Diuna --publicationYear 1992
            app.py add Trudi,Canavan --id 5311484
            app.py show 

        For more information about app.py search usage, please run:
            app.py search
            """
        parser = argparse.ArgumentParser(usage=usage)
        parser.add_argument('action')
        args, unknown = parser.parse_known_args()

        if args.action == 'search':
            del sys.argv[1]
            arguments = self.parse_arguments_search()
            books = BookSearchEngine(**vars(arguments))
            books.represent_books()
        elif args.action == 'add':
            del sys.argv[1]
            arguments = self.parse_arguments_search()
            books = BookSearchEngine(**vars(arguments))
            books.add_to_shelve()
        elif args.action == 'show':
            if len(sys.argv) > 2:
                print('*'*30, '\nYou have provided additional argument for show command. This is not supported.\n'
                      'See app.py --help for more.\n'
                      'Argument ignored.\n', '*'*30, '\n')
            BookSearchEngine.show_library_content()
        else:
            print(f'Wrong argument! Correct usage:\n{usage}')

    @staticmethod
    def parse_arguments_search() -> argparse.Namespace:
        usage_search = """
        Simple app to search for a books under Polish National library.
        The only required argument is an author.

        You can add more arguments, with following format: 
            app.py search <author> --kind e-book --publicationYear 2010

        Full list of arguments which can be used: 
        https://data.bn.org.pl/docs/bibs 

        Examples:
            app.py search Brandon,Sanders <- will print list of Brandon Sanderson's books. 
            app.py search  Sienkiewicz,Henryk --title Krzyżacy
            app.py search  Herbert,Frank --title Diuna --publicationYear 1992
            app.py search  Trudi,Canavan --kind e-book --title Nowicjuszka
            app.py search Läckberg <- it is possible to use only a surname of author

        Format of printed result:
        title: <title> 
        author: <author> 
        gentre: <gentre> 
        publicationYear: <publicationYear> 
        isbnIssn: <isbnIssn>
        id: <id>

        Example: 

        title: Krzyżacy /
        author: Sienkiewicz, Henryk (1846-1916)
        genre: Powieść polska
        publicationYear: 1995
        isbnIssn: 8370490239 8370490468
        id: 1006077
                """
        parser = argparse.ArgumentParser(usage=usage_search)
        parser.add_argument('author', type=str, help="In following format: Brandon,Sanders <- only coma separated.")

        parsed, unknown = parser.parse_known_args()
        for arg in unknown:
            if arg.startswith('--'):
                parser.add_argument(arg)

        args = parser.parse_args()
        return args


if __name__ == "__main__":
    ArgumentsParser()
