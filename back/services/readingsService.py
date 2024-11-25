from dataclasses import dataclass
from datetime import date, datetime
import json
from uuid import UUID, uuid4
from back.db.repositories.ebookRepository import EbookRepository
from back.db.repositories.readings_repository import ReadingsRepository
from back.services.libraryService import LibraryController


@dataclass
class ReadingRequest():
    ebook_guid : UUID | str
    beginning_date : str | date
    ending_date : str | date
    reading_status : int
    reading_guid : str | None = None

    def __post_init__(self):
        # Checking guid
        if isinstance(self.ebook_guid, str):
            UUID(self.ebook_guid)
        if isinstance(self.reading_guid, str):
            UUID(self.reading_guid)
        if self.reading_status not in range(1,6):
            raise ValueError("Unkown reading_status")


@dataclass
class ReadingModel():
    ebook_id : int
    beginning_date : date 
    ending_date : date | None
    reading_status_id : int
    reading_guid : str | UUID | None = None

    def __post_init__(self):
        if not self.reading_guid:
            self.reading_guid = uuid4() 
        elif isinstance(self.reading_guid, str):
            self.reading_guid = UUID(self.reading_guid)


@dataclass
class ReadingRessource():
    title : str
    author : str
    beginning_date : date 
    ending_date : date | None
    reading_status : str
    reading_guid : str

    def __repr__(self):
        return json.dumps(self.__dict__)


class ReadingsService():
    def __init__(self, conn):
        self.conn = conn

    def from_request_to_model(self, request):
        json_data = json.loads(request)
        ReadingRequest(**json_data) # validation purposes only
        json_data["ebook_id"] = EbookRepository(self.conn).get_id_from_guid(request.ebook_guid)
        del json_data["ebook_guid"]
        json_data["reading_status_id"] = json_data["reading_status"]
        del json_data["reading_status"]
        return ReadingModel(**json_data)


class ReadingsController(LibraryController):
    def __init__(self, conn, method, data):
        self.conn = conn
        self.method = method
        self.data = data
        self.repo = ReadingsRepository(self.conn)

    
    def do_GET(self):
        if not self.data:
            return 200, [ReadingRessource(*r) for r in self.repo.index()]
        if 'activate' in self.data:
            return 200, [ReadingRessource(*r) for r in self.repo.active_readings()]
        else :
            return 401, "Not Implemented either"
        

    def do_POST(self):
        repo = ReadingsRepository(self.conn)
        service = ReadingsService(self.conn)
        try:
            model = service.from_request_to_model(self.data)
            reading_guid = repo.create(model)
        except Exception as e:
            return 400, str(e)
        else:
            return 200, ReadingRessource(*repo.get_by_guid(reading_guid))
        

    def do_UPDATE(self):
        repo = ReadingsRepository(self.conn)
        service = ReadingsService(self.conn)
        try:
            model = service.from_request_to_model(self.data)
            reading_guid = repo.update(model)
        except Exception as e:
            return 400, str(e)
        else:
            return 200, ReadingRessource(*repo.get_by_guid(reading_guid))