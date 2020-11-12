import requests
import sys
import json
import argparse
import shelve
from typing import Dict


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


def lookup_for_books(author: str, **kwargs) -> Dict:
    base_url = 'https://data.bn.org.pl/api/bibs.json?'
    url = base_url + f'author={author}'

    # build url with optional arguments
    for k, v in kwargs.items():
        url += f'&{k}={v}'

    try:
        result = requests.get(url)
        result.raise_for_status()
        result = json.loads(result.text)
        bibs = result['bibs']
        return bibs
    except requests.exceptions.ConnectionError as erce:
        print(f'Ups! Something goes wrong: \n {erce}')
        exit(1)


def show_results(bibs: Dict) -> None:
    showed_elements = ['title', 'author', 'genre', 'publicationYear', 'isbnIssn', 'id']

    for book in bibs:
        for element in showed_elements:
            print(f'{element}: {book[element]}')
        print('')


def add_to_shelve(author: str, book_id: int) -> None:
    shelf_file = shelve.open('my_library')
    bibs = lookup_for_books(author, id=book_id)
    if not bibs:
        print('Ups! Book you are looking for do not exist. Did you provide correct author and id?')
    for book in bibs:
        shelf_file[book['title']] = book
        print(f'{book["title"]} has been successfully added to your library file!')
        shelf_file.close()


def show_library_content() -> None:
    shelf_file = shelve.open('my_library')
    key_list = list(shelf_file.keys())
    for key in key_list:
        print(f'{key}, {shelf_file[key]["author"]}, ISBN: {shelf_file[key]["isbnIssn"]}, ID: {shelf_file[key]["id"]}')

    books_count = len(key_list)
    print(f'\nTotal amount of books in your library: {books_count}')


def dispatcher() -> None:
    usage = """
    app.py <action> ... 

Possible actions:
app.py search <author>               <- will search for books with specified author. 
app.py show                          <- will show books in your local library file.
app.py add <author> <id>             <- will add book identified by author and id to your local library file.
    

Example:
    app.py search Sanderson,Brandon --title Elantris
    app.py search Herbert,Frank --title Diuna --publicationYear 1992
    app.py add Trudi,Canavan 5311484
    app.py show 
    
For more information about app.py search usage, please run:
    app.py search
    """
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('action')
    args, unknown = parser.parse_known_args()

    if args.action == 'search':
        del sys.argv[1]
        arguments = parse_arguments_search()
        books = lookup_for_books(**vars(arguments))
        show_results(books)
    elif args.action == 'add':
        del sys.argv[1]
        author = sys.argv[1]
        book_id = int(sys.argv[2])
        add_to_shelve(author, book_id)
    elif args.action == 'show':
        if len(sys.argv) > 2:
            print('*' * 30, '\nYou have provided additional argument for show command. This is not supported.\n'
                            'See app.py --help for more.\n'
                            'Argument ignored.\n', '*' * 30, '\n')
        show_library_content()
    else:
        print(f'Wrong argument! Correct usage:\n{usage}')


if __name__ == "__main__":
    dispatcher()
