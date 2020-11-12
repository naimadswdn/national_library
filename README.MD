Simple app to search for a books under Polish National library.
Application allow you to create your own small library. 

### How to run?
        1. approach:
            clone git repository and run app.py directly on your machine.
            Requirements: python with requests library installed.
        
        2. approach:
            use Docker to run last stable version of application:
            
            docker run --rm -v $(pwd):/app naimadswdn/national_library_app:1.0
            above command will show usage information
            
            docker run --rm -v $(pwd):/app naimadswdn/national_library_app:1.0 search Frank,Herbert
            above command will look for all Frank Herbet's books in the Polish National Library and print nice formated output.
            
            docker run -rm -v $(pwd):/app naimadswdn/national_library_app:1.0 add Canavan,Trudi 5311484
            above command will add book with id 5311484 (polish title: Nowicjuszka) into your local library file.
            (that is why you are creating a bind mount)
            
            docker run -rm -v $(pwd):/app naimadswdn/national_library_app:1.0 show
            above command will show content of your local library file.
            
            NOTE: when using 2. approach, app.py is replaced with docker run -rm -v $(pwd):/app naimadswdn/national_library_app:1.0 command.


        3. approach:
            use Docker but build image on fly:
            (not recommended)
            
            docker run --rm -v $(pwd):/app $(docker build .) search Frank,Herbert
            
            To figure out id of newly created image run: docker images 
            
            
#### SEARCH functionality:

        Running this command will search for a book records under Polish National Library.
        
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
        
#### ADD functionality:

        Running this command will add given book (identified by author and id) to your local file,
        which will be created in current directory (file:name my_library). 
        It is a binary file. To see content of your library, use show function (described below).
        
        Required arguments: author and id 
        
        General usage:
            app.py add <author> <id>
        
        Examples:
            app.py add Trudi,Canavan 5311484
            app.py add Läckberg,Camilla 2485599
            
        You can find id of a book using search functionality.
        
#### SHOW functionality:

        This funcion allow you to see content of your local library, saved under binary file my_library.
        
        Regenral usage:
            app.py show
            
        Example output:
        title: Kaznodzieja / Predikanten, Saga kryminalna Czarna Seria - Wydawnictwo Czarna Owca
        author: Läckberg, Camilla (1974- ) Sawicka, Inga Wydawnictwo Czarna Owca Läckberg, Camilla (1974- ).
        genre: Powieść szwedzka
        publicationYear: 2010
        isbnIssn: 9788375541625
        id: 2485599
        
        title: Nowicjuszka. Cz. 1 / Novice, Bestsellery fantasy ; t. 2 Trylogia Czarnego Maga ; ks. 2
        author: Canavan, Trudi (1969- ) Fulińska, Agnieszka Edipresse Polska Wydawnictwo Galeria Książki. Canavan, Trudi (1969- ). Canavan, Trudi (1969- ).
        genre: Powieść australijska
        publicationYear: 2016
        isbnIssn: 9788365534118 9788365534149
        id: 5311484
        
        Total amount of books in your library: 2