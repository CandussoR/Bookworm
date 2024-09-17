class AuthorRepository():
    def __init__(self, db):
        self.db = db


    def get_authors(self):
        q = 'SELECT full_name, birth_year, death_year, c.country, author_guid FROM authors JOIN countries c ON c.country_id = authors.country_id;'
        return self.db.execute(q).fetchall()


    def get_author(self, guid):
        q = 'SELECT full_name, birth_year, death_year, c.country, author_guid FROM authors JOIN countries ON c.country_id = authors.country_id WHERE author_guid = ?;'
        return self.db.execute(q, [guid]).fetchall()
    

    def get_id(self, name):
        '''Raise an exception if the name can't be found.'''
        id, = self.db.execute('''SELECT author_id FROM authors WHERE full_name = (?)''', [name]).fetchone()
        if not id:
            raise Exception("Author doesn't exist yet")
        return id
    

    def get_id_from_guid(self, guid) -> int:
        '''Raise an exception if the id can't be found.'''
        id, = self.db.execute('''SELECT author_id WHERE author_guid = ?''', [guid]).fetchone()
        if not id:
            raise Exception("Author not find")
        return id
    

    def get_author_by_name(self, name):
        q = '''SELECT full_name, birth_year, death_year, c.country FROM authors JOIN countries c ON c.country_id = authors.country_id WHERE full_name LIKE '%?';'''
        return self.db.execute(q, name).fetchone()


    def get_author_by_country(self, country_id):
        q = '''SELECT full_name, birth_year, death_year, c.country FROM authors WHERE country_id IS (?);'''
        return self.db.execute(q, country_id).fetchall()


    def get_contemporary_authors(self, author):
        q = '''SELECT full_name, birth_year, death_year, c.country, author_guid FROM authors WHERE birth_year BETWEEN (?) AND (?);'''
        return self.db.execute(q, [author.birth_year, author.death_year]).fetchall()


    def create(self, model, return_id : bool = False):
        ret = ''
        if return_id:
            ret = 'RETURNING author_id'
        q = f'''INSERT INTO authors (full_name, birth_year, death_year, gender_id, country_id, author_guid)
               VALUES (:full_name, :birth_year, :death_year, :gender_id, :country_id, :author_guid) {ret};''',
        self.db.execute(q, [model.__dict__])


    def update(self, model):
        return self.db.execute('''UPDATE TABLE authors (full_name, birth_year, death_year, gender_id, country_id, author_guid)
                        VALUES (:full_name, :birth_year, :death_year, :gender_id, :country_id, :author_guid)
                        RETURNING full_name, birth_year, death_year, gender_id, country_id, author_guid;''',
                        [model.__dict__]
        ).fetchone()
 

    def delete_author(self, guid):
        self.db.execute('DELETE FROM authors WHERE author_guid = ?;', [guid])