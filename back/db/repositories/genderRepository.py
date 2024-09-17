class GenderRepository():

    def __init__(self, conn):
        self.conn = conn

    def get_id_from_guid(self, guid):
        return self.conn.execute('SELECT gender_id FROM genders WHERE gender_guid = ?;', [guid]).fetchone()