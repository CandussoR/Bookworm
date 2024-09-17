from dataclasses import dataclass
import json
from uuid import UUID, uuid4
from back.db.repositories.countryRepository import CountryRepository
from back.db.repositories.crossTableRepository import CrossTableRepository
from back.db.repositories.genderRepository import GenderRepository
from back.services.baseRequest import BaseRequest
from back.services.libraryService import LibraryController
from back.db.repositories.authorRepository import AuthorRepository



class AuthorRequest(BaseRequest):

    def __init__(self, a_dict):
        self.full_name : str = ''
        self.birth_year : int | None = None
        self.death_year : int | None = None
        self.gender_guid : str | None = None
        self.country_guid : str | None = None
        self.author_guid : UUID | None = None
        self.from_json(a_dict)

        def _validate(self):
            if not self.full_name:
                raise ValueError("Full_name is required.")


@dataclass
class AuthorModel():
    full_name : str
    birth_year : int | None = None
    death_year : int | None = None
    gender_guid : str = ''
    country_guid : str = ''
    author_guid : str | None = None

    def __post_init__(self):
        if not self.author_guid:
            self.author_guid = str(uuid4())


@dataclass
class AuthorResource():
    full_name : str
    birth_year : int | None = None
    death_year : int | None = None
    country : int | None = None
    author_guid : str | None = None

    def __repr__(self):
        return json.dumps(self.__dict__)


class AuthorService():
    def __init__(self, conn):
        self.repository = AuthorRepository(conn)
        self.conn = conn

    
    def create(self, request, return_author : bool = False) -> AuthorResource | None :
        if request.gender_id:
            gender_id, = GenderRepository(self.conn).get_id_from_guid(request.gender_guid)
        if request.country_id:
            country_id, = CountryRepository(self.conn).get_id_from_guid(request.country_guid)
        model = AuthorModel(request.full_name, request.birth_year, request.death_year, gender_id, country_id, request.author_guid)
        self.repository.create(model)
        if return_author :
            author = self.repository.get_author(request.guid)
            return AuthorResource(*author)


class AuthorController(LibraryController):
    def __init__(self, conn, method, data):
        self.conn = conn
        self.repository = AuthorRepository(self.conn)
        self.method = method
        self.data = data


    def do_GET(self):
        if not self.data:
            data = self.repository.get_authors()
            authors = [AuthorResource(*d) for d in data]
            return 200, authors
        return 200, self.data
    

    def do_POST(self):
        request = AuthorRequest(*self.data)
        response = AuthorRepository(self.conn).create(request)
        if response:
            return 200, AuthorResource(*response)


    def do_PUT(self):
        request = AuthorRequest(*self.data)
        response = AuthorRepository(self.conn).update(request)
        return 200, AuthorResource(*response)
 

    def do_DELETE(self):
        if UUID(self.data):
            repo = AuthorRepository(self.conn)
            id = repo.get_id_from_guid(self.data)
            CrossTableRepository(self.conn).delete("ebooks_genres", other_id=id)
        return 200, "Successfully deleted."
