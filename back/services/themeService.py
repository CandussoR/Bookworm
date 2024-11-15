from dataclasses import dataclass
from uuid import UUID, uuid4

from back.db.repositories.crossTableRepository import CrossTableRepository
from back.db.repositories.themeRepository import ThemeRepository
from back.services.baseRequest import BaseRequest
from back.services.libraryService import LibraryController


class ThemeRequest(BaseRequest):
    def __init__(self, a_dict):
        self.theme = ''
        self.theme_guid : str | None = None
        self.from_json(a_dict)
    
    def validate(self):
        if not isinstance(self.theme, str):
            raise ValueError("Theme must be a string.")
        if self.theme_guid:
            UUID(self.theme_guid)

@dataclass
class ThemeModel():
    theme : str
    theme_guid : str | None = None

    def __post_init__(self):
        if not self.theme_guid:
            self.theme_guid = str(uuid4())

@dataclass
class ThemeResource():
    theme : str
    theme_guid : str

    def __repr__(self):
        return str(self.__dict__)


class ThemeController(LibraryController):
    '''So basic we don't really need to separate the service from Controller, there's nothing here.'''

    def __init__(self, conn, method, uri, data):
        self.method = method
        self.uri = uri
        self.data = data
        self.conn = conn

    
    def do_GET(self):
        if not self.data:
            themes = ThemeRepository(self.conn).index()
            return 200, [ThemeResource(*g) for g in themes]
        

    def do_POST(self):
        request = ThemeRequest(*self.data)
        response = ThemeRepository(self.conn).create(ThemeModel(request.theme))
        return 200, ThemeResource(*response)


    def do_PUT(self):
        request = ThemeRequest(*self.data)
        response = ThemeRepository(self.conn).update(ThemeModel(request.theme))
        return 200, ThemeResource(*response)
 

    def do_DELETE(self):
        try:
            if UUID(self.data):
                repo = ThemeRepository(self.conn)
                if UUID(self.data):
                    id = repo.get_id_from_guid(self.data)
                    CrossTableRepository(self.conn).delete("ebooks_themes", other_id=id)
                    repo.delete(self.data)
            return 200, "Successfully deleted."
        except ValueError:
            return 400, "Invalid GUID."