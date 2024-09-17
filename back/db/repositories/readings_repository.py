class ReadingsRepository():
    def __init__(self,conn):
        self.conn = conn

    
    def get_by_guid(self, guid):
        return self.conn.execute('''SELECT e.title, a.author, beginning_date, ending_date, status, reading_guid 
                          FROM readings r
                          JOIN ebooks e on e.ebook_id = r.ebook_id
                          JOIN status s ON s.status_id = r.status_id
                          Join ebooks_authors ea ON ea.ebook_id = r.ebook_id
                          JOIN authors a ON a.author_id = ea.author_id
                          WHERE reading_guid = ?;''', [guid]).fetchone()
    

    def index(self):
        return self.conn.execute('''SELECT e.title, a.author, beginning_date, ending_date, status, reading_guid 
                          FROM readings r
                          JOIN ebooks e on e.ebook_id = r.ebook_id
                          JOIN status s ON s.status_id = r.status_id
                          Join ebooks_authors ea ON ea.ebook_id = r.ebook_id
                          JOIN authors a ON a.author_id = ea.author_id;''').fetchall()
    
    

    def create(self, model):
        guid, = self.conn.execute('''INSERT INTO readings (ebook_id, beginning_date, ending_date, status_id, reading_guid)
                          VALUES (:ebook_id, :beginning_date, COALESCE(:ending_date, NULL), :status_id, :reading_guid)
                          RETURNING reading_guid;''',
                          model.__dict__).fetchone()
        return guid
    

    def update(self, model):
        q = '''UPDATE readings
                SET beginning_date = COALESCE(:beginning_date, beginning_date),
                    ending_date = COALESCE(:ending_date, ending_date),
                    status_id = COALESCE(:status_id, status_id)
                WHERE reading_guid = (:reading_guid)
                RETURNING reading_guid;'''
        guid, = self.conn.execute(q, model.__dict__).fetchone()
        return guid
    
        