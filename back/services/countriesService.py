from dataclasses import dataclass

from back.db.repositories.countryRepository import CountryRepository
from back.services.libraryService import LibraryController

@dataclass
class CountryRequest():
    pass


@dataclass
class CountryModel():
    country_id : int
    name : str
    continent_id : int


@dataclass
class CountryResource():
    name : str
    continent : int


class CountryController(LibraryController):
    def __init__(self, conn, method, data):
        self.conn = conn
        self.repository = CountryRepository(self.conn)
        self.method = method
        self.data = data
    

    def do(self):
        match self.method:
            case "GET":
                return self.do_GET()
            case "POST":
                return self.do_POST()
            case "DELETE":
                return self.do_DELETE()

    def do_GET(self):
        if not self.data:
            data = self.repository.get_countries()
            countries = [CountryResource(*d).__dict__ for d in data]
        return 200, str(countries)
    
    def do_POST(self):
        return 501, "Not implemented"

    def do_DELETE(self):
        return 501, "Not Implemented"
