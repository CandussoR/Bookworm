from dataclasses import dataclass
import json
import sqlite3
from uuid import UUID, uuid4
from back.db.repositories.ebookRepository import EbookRepository
from back.db.repositories.readingListRepository import ReadingListRepository
from back.services.libraryService import LibraryController


@dataclass
class ReadingListItem():
    title : str
    ebook_guid : UUID | str
    comment : str
    read : bool

    def __post_init__(self):
        if isinstance(self.ebook_guid, str):
            self.ebook_guid = UUID(self.ebook_guid)


@dataclass
class ReadingListModel():
    name : str
    items : list[dict] | list[ReadingListItem]
    reading_list_guid : UUID | None = None

    def __post_init__(self):
        if not self.reading_list_guid:
            self.reading_list_guid = uuid4()


class ReadingListController(LibraryController):
    def __init__(self, conn, method, data):
        self.conn = conn
        # self.service = ReadingListService(conn)
        self.method = method
        self.data = data


    def do_get(self):
        if not self.data:
            return 200, ReadingListRepository(self.conn).index()
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
    

    def do_UPDATE(self):
        req = json.loads(self.data)
        [ReadingListItem(**i) for i in req.items]
        model = ReadingListModel(**req)
        try:
            res = ReadingListRepository(self.conn).update(model)
        except Exception as e:
            return 400, str(e)
        else:
            return 200, {"name": res[0], "items": res[1], "reading_list_guid": res[2]}
    

    def do_DELETE(self, guid):
        try:
            ReadingListRepository(self.conn).delete(guid)
        except Exception as e:
            return 400, str(e)
        else :
            return 200, "Successfully deleted."