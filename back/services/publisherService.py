from dataclasses import dataclass
import json
import sqlite3
from uuid import UUID, uuid4
from back.db.repositories.publisherRepository import PublisherRepository
from back.services.baseRequest import BaseRequest
from back.services.libraryService import LibraryController


class PublisherRequest(BaseRequest):
    def __init__(self, request):
        self.publisher : str = ''
        self.publisher_guid : UUID | None = None
        self.from_json(request)
    
    def validate(self):
        if not self.publisher:
            raise ValueError("You must name a publisher.")
        if self.publisher_guid and not isinstance(self.publisher_guid, UUID):
            raise ValueError("GUID is not valid.")


@dataclass
class PublisherModel:
    publisher : str
    publisher_guid : str | None = None

    def __post_init__(self):
        if not self.publisher_guid:
            self.publisher_guid = str(uuid4())
        else:
            UUID(self.publisher_guid)


@dataclass
class PublisherResource:
    publisher : str
    publisher_guid : str

    def __repr__(self):
        return json.dumps(self.__dict__)
    
    

class PublisherController(LibraryController):
    def __init__(self, conn, method, uri, data):
        self.conn = conn
        self.method = method
        self.uri = uri
        self.data = data


    def do_GET(self):
        '''Takes no data or a guid.'''
        repo = PublisherRepository(self.conn)
        try: 
            if not self.data:
                publishers = repo.index()
                return 200, [PublisherResource(*p) for p in publishers]
            elif UUID(self.data):
                    pub = repo.get(self.data)
                    return 200, PublisherResource(*pub)
        except ValueError :
            return 400, "Invalid GUID."

    
    def do_POST(self):
        try:
            request = PublisherRequest(self.data)
            response = PublisherRepository(self.conn).create(PublisherModel(request.publisher))
            return 200, PublisherResource(*response)
        except ValueError:
            return 400, "Invalid GUID"
        except sqlite3.OperationalError as e:
            return 400, str(e)
        
    
    def do_PUT(self):
        try:
            request = PublisherRequest(self.data)
            if not request.publisher_guid:
                return 400, "GUID is missing."
            model = PublisherModel(request.publisher, request.publisher_guid) #type: ignore
            response = PublisherRepository(self.conn).update(model)
            return 200, PublisherResource(*response)
        except ValueError:
            return 400, "Invalid GUID"
        except sqlite3.OperationalError as e:
            return 400, str(e)


    def do_DELETE(self):
        try:
            if UUID(self.data):
                PublisherRepository(self.conn).delete(self.data)
            return 200, "Successfully deleted"
        except ValueError:
            return 400, "Invalid GUID."