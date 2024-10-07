from dataclasses import asdict, dataclass
import json
import sqlite3
from uuid import UUID, uuid4
from back.db.repositories.ebookRepository import EbookRepository
from back.db.repositories.readingListRepository import ReadingListRepository
from back.services.ebookService import EbookService
from back.services.libraryService import LibraryController


@dataclass
class ReadingListItem():
    title : str
    author: str
    ebook_guid : UUID | str
    comment : str
    read : bool

    def __post_init__(self):
        if isinstance(self.ebook_guid, str):
            self.ebook_guid = UUID(self.ebook_guid)


@dataclass
class ReadingListModel():
    name : str
    description : str
    items : list[dict] | list[ReadingListItem]
    reading_list_guid : UUID | None = None

    def __post_init__(self):
        if not self.reading_list_guid:
            self.reading_list_guid = uuid4()


@dataclass
class ReadingListRessource():
    name : str
    items : str
    reading_list_guid : str
    description : str | None = None


class ReadingListService():
    def __init__(self, conn):
        self.conn = conn
        self.repo = ReadingListRepository(self.conn)


    def update(self, req):
        try:
            if req["items"]["action"] == "add":
                repo = EbookRepository(self.conn)
                id = repo.get_id_from_guid(req["items"]["val"])
                title, author, guid = repo.get_ebook_for_reading_list(id)
                req["items"]["content"] = json.dumps({
                                "title": title,
                                "author": author,
                                "ebook_guid": guid,
                                "comment": None,
                                "read": 0
                            })                    

            # If action is neither delete or add, it's an update
            self.repo.update(req)
            name, description, items, reading_list_guid = self.repo.get(req["reading_list_guid"])
            return ReadingListRessource(name, items, reading_list_guid, description).__dict__
        except (TypeError, sqlite3.ProgrammingError) as e:
            import traceback
            print(traceback.print_exc())

class ReadingListController(LibraryController):
    def __init__(self, conn, method, data):
        self.conn = conn
        self.method = method
        self.data = data

    def do_GET(self):
        if not self.data:
            reading_lists = ReadingListRepository(self.conn).index() 
            ressource = []
            for (name, description, reading_list, reading_list_guid) in reading_lists:
                ressource.append(
                    ReadingListRessource(
                        name=name,
                        description=description,
                        items=json.loads(reading_list),
                        reading_list_guid=reading_list_guid,
                    )
                )
            print("ressource\n", ressource)
            return 200, json.dumps({"reading_lists" : [asdict(r) for r in ressource]})
        else : 
            return 200, ReadingListRepository(self.conn).get(self.data)

    def do_POST(self):
        reading_list = json.loads(self.data)

        # Just validating the guids
        [ReadingListItem(**i) for i in reading_list.items]

        model = ReadingListModel(**reading_list)

        try :
            res = ReadingListRepository(self.conn).create(model)
        except sqlite3.OperationalError as e:
            return 400, str(e)
        else:
            return 200, res

    def do_PUT(self):
        req = json.loads(self.data)
        # Throwing an error, validation. Only useful for requests from API client like Postman, because front will be good.
        UUID(req["reading_list_guid"])

        try:
            res = ReadingListService(self.conn).update(req)
        except Exception as e:
            return 400, str(e)
        else:
            return 200, res

    def do_DELETE(self, guid):
        try:
            ReadingListRepository(self.conn).delete(guid)
        except Exception as e:
            return 400, str(e)
        else :
            return 200, "Successfully deleted."
