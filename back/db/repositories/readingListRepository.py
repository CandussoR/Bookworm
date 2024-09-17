class ReadingListRepository():
    def __init__(self, conn):
        self.conn = conn


    def index(self):
        return self.conn.execute('''SELECT name, items, reading_list_guid FROM reading_lists;''').fetchall()


    def get(self, reading_list_guid):
        return self.conn.execute('''SELECT name, items, reading_list_guid FROM reading_lists WHERE reading_list_guid = ?;''',
                                 [reading_list_guid]).fetchone()


    def create(self, model):
        return self.conn.execute('''INSERT INTO reading_lists (name, items, reading_list_guid) 
                                 VALUES (:name, :items, :reading_list_guid) 
                                 RETURNING name, items, reading_list_guid;''', 
                                 model.__dict__).fetchone()        


    def update(self, model):
        return self.conn.execute("""UPDATE TABLE reading_lists 
                                 SET name = (:name) AND items = (:items) 
                                 WHERE reading_list_guid = (:reading_list_guid) 
                                 RETURNING name, items, reading_list_guid;""",
                                model.__dict__).fetchone()


    def delete(self, reading_list_guid):
        self.conn.execute('DELETE FROM reading_lists WHERE reading_list_guid = ?;', [reading_list_guid])
