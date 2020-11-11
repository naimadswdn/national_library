import requests
import sys
import json
import argparse


def parse_arguments():
    usage = """
Simple app to search for a books under Polish National library.
The only required argument is an author.
        
You can add more arguments, with following format: 
    app.py <author> --kind e-book --publicationYear 2010

Full list of arguments which can be used: 
https://data.bn.org.pl/docs/bibs 

Examples:
    app.py Brandon,Sanders <- will print list of Brandon Sanderson's books. 
    app.py Sienkiewicz,Henryk --title Krzyżacy
    app.py Herbert,Frank --title Diuna --publicationYear 1992
    app.py Trudi,Canavan --kind e-book --title Nowicjuszka
    
Format of printed result:
title: <title> 
author: <author> 
gentre: <gentre> 
publicationYear: <publicationYear> 
isbnIssn: <isbnIssn>

Example: 

title: Krzyżacy /
author: Sienkiewicz, Henryk (1846-1916)
genre: Powieść polska
publicationYear: 1995
isbnIssn: 8370490239 8370490468
        """
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('author', type=str, help="In following format: Brandon,Sanders <- only coma separated.")

    parsed, unknown = parser.parse_known_args()

    for arg in unknown:
        if arg.startswith('--'):
            parser.add_argument(arg)

    args = parser.parse_args()

    return args


def lookup_for_books(author, **kwargs):
    base_url = 'https://data.bn.org.pl/api/bibs.json?'
    url = base_url + f'author={author}'

    # build url with optional arguments
    print(kwargs)
    for k, v in kwargs.items():
        print(f'{k}: {v}')
        url += f'&{k}={v}'

    print(url)

    result = requests.get(url)
    result.raise_for_status()
    result = json.loads(result.text)

    bibs = result['bibs']

    return bibs


def show_results(bibs):
    showed_elements = ['title', 'author', 'genre', 'publicationYear', 'isbnIssn']

    for book in bibs:
        for element in showed_elements:
            print(f'{element}: {book[element]}')
        print('')


if __name__ == "__main__":
    arguments = parse_arguments()
    result = lookup_for_books(**vars(arguments))
    show_results(result)

