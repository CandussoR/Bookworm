class CountryRepository():
    def __init__(self, conn):
        self.db = conn
    

    def get_countries(self):
        return self.db.execute('SELECT countries.country, continents.continent FROM countries JOIN continents ON countries.continent_id = continents.continent_id;').fetchall()
    

    def get_id_from_guid(self, guid):
        return self.db.execute('SELECT country_id FROM countries WHERE country_guid = ?;', [guid]).fetchone()