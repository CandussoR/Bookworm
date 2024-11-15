from dataclasses import dataclass
from uuid import UUID, uuid4

from back.db.repositories.crossTableRepository import CrossTableRepository
from back.db.repositories.genreRepository import GenreRepository
from back.services.baseRequest import BaseRequest
from back.services.libraryService import LibraryController


class GenreRequest(BaseRequest):
    def __init__(self, a_dict):
        self.genre = ''
        self.genre_guid : str | None = None
        self.from_json(a_dict)
    
    def validate(self):
        if not isinstance(self.genre, str) :
            raise ValueError("Genre must be a string.")
        if self.genre_guid:
            UUID(self.genre_guid)

@dataclass
class GenreModel():
    genre : str
    genre_guid : str | None = None

    def __post_init__(self):
        if not self.genre_guid:
            self.genre_guid = str(uuid4())

@dataclass
class GenreResource():
    genre : str
    genre_guid : str

    def __repr__(self):
        return str(self.__dict__)


class GenreController(LibraryController):
    '''So basic we don't really need to separate the service from Controller, 
    there's nothing here.'''

    def __init__(self, conn, method, uri, data):
        self.method = method
        self.uri = uri
        self.data = data
        self.conn = conn

    
    def do_GET(self):
        if not self.data:
            genres = GenreRepository(self.conn).index()
            return 200, [GenreResource(*g) for g in genres]

    
    def do_POST(self):
        request = GenreRequest(*self.data)
        response = GenreRepository(self.conn).create(GenreModel(request.genre))
        return 200, GenreResource(*response)


    def do_PUT(self):
        request = GenreRequest(*self.data)
        response = GenreRepository(self.conn).update(GenreModel(request.genre))
        return 200, GenreResource(*response)
 

    def do_DELETE(self):
        if UUID(self.data):
            repo = GenreRepository(self.conn)
            if UUID(self.data):
                id = repo.get_id_from_guid(self.data)
                CrossTableRepository(self.conn).delete("ebooks_genres", 
                                                       other_id=id)
                repo.delete(self.data)
        return 200, "Successfully deleted."