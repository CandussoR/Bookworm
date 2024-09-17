class CrossTableRepository():
    second_column = {
        "ebooks_themes": "theme_id",
        "ebooks_genres": "genre_id",
        "ebooks_authors": "author_id",
    }


    def __init__(self, conn):
        self.conn = conn


    def get(self, table, ebook_id = None, other_id = None) -> list[tuple]:
        if table not in self.second_column:
            raise Exception("Table doesn't exist.")
        return self.conn.execute(f'SELECT ebook_id, {self.second_column["table"]} WHERE ebook_id = ?', [ebook_id]).fetchall()
        

    def create(self, table, ids : list[tuple[int, int]]):
        if table not in self.second_column:
            raise Exception("Table doesn't exist.")
        for ebook_id, other_id in ids:
            self.conn.execute(f"""INSERT INTO { table } (ebook_id, { self.second_column[table] }) VALUES ( ?, ? );""",
                [ebook_id, other_id],
            )


    def delete(self, table, ebook_id : int | None = None, other_id : int | None = None):
        """Will send operational error if infos doesn't match."""
        if not table in self.second_column:
            raise ValueError("Table doesn't exist.")
        query = ''
        if not ebook_id:
            query, params = (f'''DELETE FROM {table} WHERE {self.second_column[table]} = ?''', [other_id])
        elif ebook_id and not other_id:
            query, params = (f'''DELETE FROM {table} WHERE ebook_id = ?''', [ebook_id])
        else :
            query, params = (f'''DELETE FROM {table} WHERE ebook_id = ebook_id AND {self.second_column[table]} = (?)''', [ebook_id, other_id])

        self.conn.execute(query, params)
