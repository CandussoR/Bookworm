from sqlite3 import Connection
import sqlite3
class ReadingListRepository():
    def __init__(self, conn : Connection):
        self.conn = conn

    def index(self) -> list[tuple]:
        return self.conn.execute(
            """SELECT name, description, items, reading_list_guid FROM reading_lists;"""
        ).fetchall()

    def get(self, reading_list_guid):
        return self.conn.execute(
            """SELECT name, description, items, reading_list_guid 
               FROM reading_lists 
               WHERE reading_list_guid = ?;""",
            [reading_list_guid],
        ).fetchone()

    def create(self, model):
        return self.conn.execute(
            """INSERT INTO reading_lists (name, description, items, reading_list_guid) 
                                 VALUES (:name, :description, :items, :reading_list_guid) 
                                 RETURNING name, description, items, reading_list_guid;""",
            model.__dict__,
        ).fetchone()

    def update(self, req: dict) -> None:
        '''
        Gets a req dictionary where items have been converted into a list of 
        tuples, return nothing.'''

        if not "reading_list_guid" in req:
            raise ValueError("We need at least a guid for an update.")

        if "items" in req:
            match(req["items"]["action"]):
                case "delete":
                    self.conn.execute(
                        """UPDATE reading_lists
                        SET items = json_remove(items, ?)
                        WHERE reading_list_guid = ?;""",
                        (f'$[{req["items"]["i"]}]', req["reading_list_guid"]),
                    )
                case "add":
                    self.conn.execute(
                        '''UPDATE reading_lists 
                        SET items = json_set(items, '$[#]', json(?))
                        WHERE reading_list_guid = ?;''',
                        (req["items"]["content"],  req["reading_list_guid"])
                    )
                case "update":
                    self.conn.execute(
                        """UPDATE reading_lists 
                        SET items = json_set(items, ?, json(?)) 
                        WHERE reading_list_guid = ?;""",
                        (
                            f'$[{req["items"]["i"]}].{req["items"]["key"]}',
                            req["items"]["val"],
                            req["reading_list_guid"],
                        ),
                    )

        elif "name" in req:
            self.conn.execute(
                '''UPDATE reading_lists
                SET name = COALESCE(:name, name)
                WHERE reading_list_guid = (:reading_list_guid);''',
                req.__dict__,
            )
        elif "description" in req:
            self.conn.execute(
                '''UPDATE reading_lists 
                SET description = COALESCE(:description, description)
                WHERE reading_list_guid = (:reading_list_guid);''',
                req.__dict__,
            )

    def delete(self, reading_list_guid):
        self.conn.execute(
            'DELETE FROM reading_lists WHERE reading_list_guid = ?;',
            [reading_list_guid]
            )
