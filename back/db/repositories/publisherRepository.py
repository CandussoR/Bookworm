class PublisherRepository():
    def __init__(self, conn):
        self.conn = conn


    def index(self):
        return self.conn.execute('SELECT publisher, publisher_guid FROM publishers;').fetchall()


    def get(self, guid : str | None = None, id : str | None = None):
        if guid and id:
            raise ValueError("It's either guid or id, not both.")
        if guid:
            return self.conn.execute('SELECT publisher, publisher_guid FROM publishers WHERE publisher_guid = ?;', [guid]).fetchone()
        elif id:
            return self.conn.execute('SELECT publisher, _publisher_guid FROM publishers WHERE publisher_id = ?;', [id]).fetchone()


    def get_id(self, name) -> int:
        return self.conn.execute('SELECT publisher_id FROM publishers WHERE publisher = (?);', [name]).fetchone()


    def create(self, model):
        '''Takes a model and returns a tuple for the PublisherResource.'''
        return self.conn.execute(
            """INSERT INTO publishers (publisher, publisher_guid) VALUES (:publisher, :publisher_guid)
            RETURNING publisher_id;""",
            model.__dict__,
        ).fetchone()


    def update(self, model):
        '''Takes a model and returns a tuple for the PublisherResource.'''
        return self.conn.execute(
            '''UPDATE TABLE publishers SET publisher = :publisher WHERE publisher_guid = :publisher_guid
            RETURNING publisher, publisher_guid;''',
            model.__dict__
        ).fetchone()
    

    def delete(self, guid):
        self.conn.execute('DELETE FROM publishers WHERE publisher_guid = ?;', [guid])