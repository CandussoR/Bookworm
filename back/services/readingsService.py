from dataclasses import dataclass
from datetime import date, datetime
import json
from uuid import UUID, uuid4
from back.db.repositories.ebookRepository import EbookRepository
from back.db.repositories.readings_repository import ReadingsRepository
from back.services.libraryService import LibraryController


@dataclass
class ReadingRequest():
    '''When request is for a create, ebook_guid needed and no reading_guid ;
    when request is for update, reading_guid needed and no ebook_guid.'''
    beginning_date : str
    ending_date : str
    reading_status : int
    ebook_guid : UUID | str | None = None
    reading_guid : str | None = None

    def __post_init__(self):
        # Checking guid
        if self.ebook_guid and self.reading_guid:
            raise ValueError("Can't have both guids in there.")
        if isinstance(self.ebook_guid, str):
            UUID(self.ebook_guid)
        if isinstance(self.reading_guid, str):
            UUID(self.reading_guid)
        if self.reading_status not in range(1,6):
            raise ValueError("Unkown reading_status")
        if self.beginning_date and self.ending_date and (self.beginning_date > self.ending_date):
            raise ValueError("Beginning date comes after ending date.")


@dataclass
class ReadingModel():
    beginning_date : date 
    ending_date : date | None
    reading_status_id : int
    ebook_id : int | None = None
    reading_guid : str | None = None

    def __post_init__(self):
        # Only have ebook_id when creating, only have reading_guid when updating
        if self.reading_guid and self.ebook_id:
            raise ValueError("We either have an ebook_id or a reading_guid.")
        if not self.reading_guid:
            self.reading_guid = str(uuid4())


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

    def from_request_to_model(self, request, is_update = False):
        json_data = json.loads(request)
        ReadingRequest(**json_data) # validation purposes only
        if not is_update:
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
        if 'active' in self.data:
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
        

    def do_PUT(self):
        repo = ReadingsRepository(self.conn)
        service = ReadingsService(self.conn)
        try:
            model = service.from_request_to_model(self.data, is_update=True)
            repo.update(model)
        except Exception as e:
            return 400, str(e)
        else:
            # Returning only the active readings to update the front component all at once
            return 200, [ReadingRessource(*r) for r in self.repo.active_readings()]