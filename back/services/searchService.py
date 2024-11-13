import json
from back.db.repositories.authorRepository import AuthorRepository
from back.db.repositories.genreRepository import GenreRepository
from back.db.repositories.themeRepository import ThemeRepository
from back.services.authorService import AuthorService
from back.services.libraryService import LibraryController


class SearchController(LibraryController):
    """This class is for now only use in the EditMetadata component of the front.
    Each request that comes in only tries to find matches in author, publisher, theme, genre tables.
    """
    def __init__(self, db, method, data):
        self.db = db
        self.method = method
        self.data = data

    def do_GET(self):
        print("SearchController received this data", self.data)
        data = None
        match(self.data[0]):
            case "author":
                data = AuthorRepository(self.db).search(self.data[1])
            case "genre":
                data = GenreRepository(self.db).search(self.data[1])
            case "theme":
                data = ThemeRepository(self.db).search(self.data[1])
            case _:
                return 500, "Research impossible : error in key."
        return 200, json.dumps([d for d, in data])
        # return 200, "Did search"
