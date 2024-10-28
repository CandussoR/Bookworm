'''
    To run this test, execute:
        python -m back.test.testEbook
'''

import unittest

from back.db import sqlite_db
from back.services.ebookService import EbookController, EbookService
from .data_mock import mock

class TestEbookService(unittest.TestCase):
    def setUp(self):
        # Setup for bdd
        self.db = sqlite_db.connect(':memory:')
        self.db.executescript(sqlite_db.tables)
        self.db.executescript(mock)

    def tearDown(self):
        self.db.close()

    def test_index_returns_all_books(self):
        controller = EbookController(self.db, "GET", None)
        code, result = controller.do_GET()
        self.assertEqual(code, 200)
        self.assertEqual(len(result), 2)


    def test_delete_wipes_book_if_not_in_readings(self):
        controller = EbookController(self.db, "DELETE", '4f4ce7e2-e0b3-42c4-83b9-2efee80baeb5')
        res = controller.do_DELETE()
        get_result = EbookService(self.db).index()
        self.assertEqual(res, (200, "Successfully deleted."))
        self.assertEqual(len(get_result), 1, str(get_result))


    def test_delete_does_not_wipe_book_if_in_readings(self):
        controller = EbookController(self.db, "DELETE", '4f4ce8e2-e0b3-42c4-83b9-2efee80baeb4')
        res = controller.do_DELETE()
        count_remaining_books, = self.db.execute('SELECT COUNT(ebook_id) FROM ebooks;').fetchone()
        self.assertEqual(res, (200, "Successfully deleted."))
        self.assertEqual(count_remaining_books, 2, str(count_remaining_books)) 

if __name__ == '__main__':
    unittest.main()