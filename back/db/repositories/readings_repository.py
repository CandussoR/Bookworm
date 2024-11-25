class ReadingsRepository():
    def __init__(self,conn):
        self.conn = conn

    
    def get_by_guid(self, guid):
        return self.conn.execute('''SELECT e.title, GROUP_CONCAT(a.full_name, ', ') as author, beginning_date, ending_date, s.reading_status, reading_guid 
                          FROM readings r
                          JOIN ebooks e on e.ebook_id = r.ebook_id
                          JOIN reading_status s ON s.reading_status_id = r.reading_status_id
                          Join ebooks_authors ea ON ea.ebook_id = r.ebook_id
                          JOIN authors a ON a.author_id = ea.author_id
                          WHERE reading_guid = ?;''', [guid]).fetchone()
    
    
    def is_ebook_read(self, ebook_id) :
        '''Used to check how to delete a book or to give more infos about it.'''
        return self.conn.execute('''SELECT ebook_id FROM readings WHERE ebook_id = ?''', [ebook_id]).fetchall()


    def index(self):
        return self.conn.execute('''SELECT e.title, GROUP_CONCAT(a.full_name, ', ') as author, beginning_date, ending_date, s.reading_status, reading_guid 
                          FROM readings r
                          JOIN ebooks e on e.ebook_id = r.ebook_id
                          JOIN reading_status s ON s.reading_status_id = r.reading_status_id
                          JOIN ebooks_authors ea ON ea.ebook_id = r.ebook_id
                          JOIN authors a ON a.author_id = ea.author_id;''').fetchall()
    

    def active_readings(self):
        return self.conn.execute('''SELECT e.title, GROUP_CONCAT(a.full_name, ', ') as author, beginning_date, ending_date, s.reading_status, reading_guid 
                          FROM readings r
                          JOIN ebooks e on e.ebook_id = r.ebook_id
                          JOIN reading_status s ON s.reading_status_id = r.reading_status_id
                          JOIN ebooks_authors ea ON ea.ebook_id = r.ebook_id
                          JOIN authors a ON a.author_id = ea.author_id
                          WHERE r.reading_status_id = 1;''').fetchall()
    

    def create(self, model):
        guid, = self.conn.execute('''INSERT INTO readings (ebook_id, beginning_date, ending_date, reading_status_id, reading_guid)
                          VALUES (:ebook_id, :beginning_date, COALESCE(:ending_date, NULL), :reading_status_id, :reading_guid)
                          RETURNING reading_guid;''',
                          model.__dict__).fetchone()
        return guid
    

    def update(self, model):
        q = '''UPDATE readings
                SET beginning_date = COALESCE(:beginning_date, beginning_date),
                    ending_date = COALESCE(:ending_date, ending_date),
                    reading_status_id = COALESCE(:reading_status_id, reading_status_id)
                WHERE reading_guid = (:reading_guid)
                RETURNING reading_guid;'''
        guid, = self.conn.execute(q, model.__dict__).fetchone()
        return guid
    
        