
class ThemeRepository():
    def __init__(self, conn):
        self.conn = conn
    

    def index(self):
        return self.conn.execute('SELECT theme, theme_guid FROM themes;').fetchall()
    

    def get_id(self, theme):
        id, = self.conn.execute('''SELECT theme_id FROM themes WHERE theme = (?)''', [theme]).fetchone()
        if not id:
            raise Exception("Theme doesn't exist yet.")
        return id
    

    def get_id_from_guid(self, guid) -> int:
        id, = self.conn.execute(f'SELECT theme_id WHERE theme_guid = ?;', guid).fetchone()
        if not id:
            raise Exception("No theme linked to this guid.")
        return id
    
    
    def create(self, model):
        return self.conn.execute('''INSERT INTO themes (theme, theme_guid) VALUES :theme, :theme_guid RETURNING theme, theme_guid RETURNING theme_id;''', [model.__dict__]).fetchone()
    
    
    def update(self, model):
        return self.conn.execute('''UPDATE TABLE themes SET theme = :theme WHERE guid = :theme_guid RETURNING theme, theme_guid;''', [model.__dict__]).fetchone()
    
    
    def delete(self, guid):
        self.conn.execute('DELETE FROM themes WHERE theme_guid = (?);', [guid])