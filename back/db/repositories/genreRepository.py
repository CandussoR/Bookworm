class GenreRepository():
    def __init__(self, conn):
        self.conn = conn
    

    def index(self):
        return self.conn.execute('SELECT genre, genre_guid FROM genres;').fetchall()


    def get_id(self, genre):
        id, = self.conn.execute('''SELECT genre_id FROM genres WHERE genre = (?)''', [genre]).fetchone()
        if not id:
            raise Exception("Genre doesn't exist yet.")
        return id
    

    def get_id_from_guid(self, guid) -> int:
        id, = self.conn.execute('SELECT genre_id FROM genre WHERE genre_guid = ?', [guid]).fetchone()
        if not id:
            raise Exception("No genre linked to the guid.")
        return id
    

    def create(self, model):
        return self.conn.execute('''INSERT INTO genres (genre, genre_guid) VALUES (:genre, :genre_guid) RETURNING genre, genre_guid RETURNING genre_id;''', [model.__dict__]).fetchone()

    def update(self, model):
        return self.conn.execute('''UPDATE TABLE genres SET genre = :genre WHERE genre_guid = :genre_guid RETURNING genre, genre_guid;;''', [model.__dict__]).fetchone()


    def delete(self, guid):
        self.conn.execute('DELETE FROM genres WHERE genre_guid = ?', [guid])