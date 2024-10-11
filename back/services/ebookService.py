from dataclasses import dataclass
from functools import lru_cache
import sqlite3
from uuid import UUID, uuid4
import json
from back.db.repositories.authorRepository import AuthorRepository
from back.db.repositories.crossTableRepository import CrossTableRepository
from back.db.repositories.genreRepository import GenreRepository
from back.db.repositories.publisherRepository import PublisherRepository
from back.db.repositories.themeRepository import ThemeRepository
from back.services.authorService import AuthorModel
from back.services.baseRequest import BaseRequest
from back.services.genreService import GenreModel
from back.services.libraryService import LibraryController
from back.db.repositories.ebookRepository import EbookRepository
from back.services.themeService import ThemeModel


class EbookRequest(BaseRequest):
    def __init__(self, json_data):            
        self.title : str = ''
        self.author : list[str] = []
        self.publisher : str = ''
        self.year_of_publication : int = 0
        self.genre : list[str] = []
        self.theme : list[str] = []
        self.ebook_guid : UUID | None = None

        self.from_json(json_data)

    
    def validate(self) -> None:
        if not (self.title and self.publisher and self.year_of_publication):
            raise ValueError("Forbidden values in request")
        if self.ebook_guid and not isinstance(self.ebook_guid, UUID):
            raise ValueError("Guid is not valid")



@dataclass
class EbookModel():
    title : str
    publisher_id : int 
    year_of_publication : int
    ebook_guid : str
    
    def new_guid(self):
        self.ebook_guid = str(uuid4())


@dataclass
class EbookResource():
    title : str
    author : str
    year_of_publication : int
    publisher : str
    genre : str
    theme : str
    ebook_guid : str
    country: str = ''

    def __post_init__(self):
        for k,v in self.__dict__.items():
            if k in ["author", "genre", "theme"]:
                if v is not None:
                    setattr(self, k, v.split(','))
                else:
                    setattr(self, k, None)
        if not self.country:
            delattr(self, "country")
        

    def __repr__(self):
        return json.dumps(self.__dict__)


@dataclass
class EbookSearchResult:
    title : str
    author : str
    ebook_guid : str

    def __repr__(self):
        return json.dumps(self.__dict__)


class EbookService():
    '''All the fun stuff happening related to Ebooks.'''

    def __init__(self, conn):
        self.conn = conn
        self.repository = EbookRepository(conn)

    @lru_cache(maxsize = 1)
    def index(self) -> list[EbookResource]:
        data = self.repository.get_ebooks()
        return [EbookResource(*d) for d in data] if data else []


    def get_by(self, key, value) -> list[EbookResource]:
        data = self.repository.get_ebooks_by(key, value)
        return [EbookResource(*d) for d in data] if data else []


    def search(self, query):
        data = self.repository.search(query)
        return [EbookSearchResult(*d) for d in data] if data else []
    

    def create(self, request : EbookRequest) -> EbookResource:
        author_repo = AuthorRepository(self.conn)
        genre_repo = GenreRepository(self.conn)
        theme_repo = ThemeRepository(self.conn)
        cross_tables_repo = CrossTableRepository(self.conn)

        authors_id = []
        genres_id = []
        themes_id = []
        for k,v in request.__dict__.items(): 
            v = [v] if not isinstance(v, list) else v          
            match k:
                case "author":
                    authors_id = self._get_ids(k, author_repo, v)
                case "genre":
                    genres_id = self._get_ids(k, genre_repo, v)
                case "theme":
                    themes_id = self._get_ids(k, theme_repo, v)
                case "publisher":
                    # There's only one publisher every time for now
                    [publisher_id] = self._get_ids(k, PublisherRepository(self.conn), v)
        model = EbookModel(request.title, publisher_id, request.year_of_publication, str(request.ebook_guid))
        ebook_id = self._create_ebook(model)

        cross_tables_repo.create("ebooks_authors", [(ebook_id, a) for a in authors_id])
        cross_tables_repo.create("ebooks_themes", [(ebook_id, t) for t in themes_id])
        cross_tables_repo.create("ebooks_genres", [(ebook_id, g) for g in genres_id])

        data = self.repository.get_ebook(ebook_id)
        return EbookResource(*data)
    

    def update(self, request):
        '''Handle an update request which might be only minimal with Model fields,
        or greater if other fields are modified.'''
        ebook_id = self.repository.get_id_from_guid(request.ebook_guid)

        for v in ["author", "theme", "genre"]:
            if v in request:
                repo = self._create_repo(v)
                ids= [repo.get_id_from_guid(v) for v in request[v]]
                self._update_cross_table(f"ebooks_{v}s", ebook_id, ids)
        
        model = EbookModel(request.title, request.publisher_id, request.year_of_publication, request.ebook_guid)
        self.repository.update(model)
        data = self.repository.get_ebook(ebook_id)
        return EbookResource(*data)
    
    
    def delete(self, guid):
        UUID(guid)
        ebook_id = self.repository.get_id_from_guid(guid)
        ct_repo = CrossTableRepository(self.conn)
        for table in ["ebooks_authors", "ebooks_themes", "ebooks_genres"]:
            ct_repo.delete(table, ebook_id)
        self.repository.delete(guid)

    
    def _create_repo(self, key):
        if key == "author":
            return AuthorRepository(self.conn)
        elif key == "genre":
            return GenreRepository(self.conn)
        elif key == "theme":
            return ThemeRepository(self.conn)
        else:
            raise KeyError("This key isn't possible")
        

    def _get_ids(self, key, repo, values : list[str]):
            ids = []
            for v in values:
                id = repo.get_id(v)
                if not id:
                    id, = repo.create(self._create_model(key,v))
                else:
                    # Unpacking the tuple only now since unpacking None raises a TypeError
                    id = id,
                ids.append(id)
            return ids
    
    def _create_ebook(self, model : EbookModel) -> int:
        while True:
            try:
                ebook_id = self.repository.create(model)
                break
            # If guid is not unique per curse
            except sqlite3.IntegrityError:
                model.new_guid()
        return ebook_id
    

    def _create_model(self, key, v):
        if key == "author":
            return AuthorModel(full_name=v)
        elif key == "genre":
            return GenreModel(genre=v)
        elif key == "theme":
            return ThemeModel(theme=v)
        else:
            raise KeyError("This key isn't possible") 
        

    def _update_cross_table(self, table, ebook_id, other_ids):
        '''Ensuring that a foreign key constraint won't interfere with our plans of eradication.'''
        repo = CrossTableRepository(self.conn)
        # Get the ranks thanks to ebook_id
        ranks = repo.get(table, ebook_id)
        # Compare the ids paired with the ebook
        # If some values are not present in the update, delete those
        for v in ranks:
            _, o_id = v
            if not o_id in other_ids:
                repo.delete(table, ebook_id, o_id)
        # If some values are not present in the old ranks, add those
        old_ids = [o_id for (_, o_id) in ranks]
        for i in other_ids:
            if not i in old_ids:
                repo.create(table, [(ebook_id, i)])
        # Guess we're done


class EbookController(LibraryController):
    '''Routing only.'''

    def __init__(self, conn, method, data):
        self.service = EbookService(conn)
        self.method = method
        self.data = data


    def do_GET(self):
        '''Gets either no data or an array of key, value'''
        try :
            if not self.data:
                return 200, self.service.index()
            elif self.data and self.data[0] == 'search':
                return 200, self.service.search(self.data[1]) 
            else :
                return 200, self.service.get_by(*self.data)
        except sqlite3.OperationalError as e:
            return 500, f"An error occurred. ${str(e)}"



    def do_POST(self):
        try:
            data = json.loads(self.data)
            resource = self.service.create(EbookRequest(data))
        except Exception as e:
            return 400, str(e)
        else:
            return 200, resource
        

    def do_PUT(self):
        resource = self.service.update(EbookRequest(self.data))
        return 200, resource


    def do_DELETE(self):
        try:
            self.service.delete(self.data)
        except ValueError as e:
            return 400, str(e)
        else:
            return 200, "Successfully deleted."