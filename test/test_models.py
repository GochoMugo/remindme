'''
Testing models.

Objectives:
 - ensure a consistent interface is maintained
'''

import unittest
from remindme.models import Remindme, RemindmeDatabase


class Test_Remindme_Model(unittest.TestCase):
    '''Tests against the Remindme model (remindme.models.Remindme).'''

    def setUp(self):
        self.title = "some title"
        self.content = "some content"
        self.db = RemindmeDatabase("./test/_test.Remindme.db")
        self.remindme = Remindme(self.title, self.content, self.db)

    def test_constructor_sets_title(self):
        self.assertEqual(self.title, self.remindme.title(),
            "constructor fails to set title of remindme")

    def test_constructor_sets_content(self):
        self.assertEqual(self.content, self.remindme.content(),
            "constructor fails to set content of remindme")

    def test_constructor_sets_db(self):
        self.assertEqual(self.db, self.remindme.database(),
            "constructor fails to set database of remindme")

    def test_title_gets_title(self):
        self.assertEqual(self.title, self.remindme.title(),
            "Remindme#title([title]) fails to get title of remindme")

    def test_title_sets_title(self):
        self.title = "new title, dummy!"
        self.remindme.title(self.title)
        self.assertEqual(self.title, self.remindme.title(),
            "Remindme#title([title]) fails to set title of remindme")

    def test_content_gets_content(self):
        self.assertEqual(self.content, self.remindme.content(),
            "Remindme#content([content]) fails to get content of remindme")

    def test_content_sets_content(self):
        self.content = "new content, dummy!"
        self.remindme.content(self.content)
        self.assertEqual(self.content, self.remindme.content(),
            "Remindme#content([content]) fails to set content of remindme")

    def test_database_gets_database(self):
        self.assertEqual(self.db, self.remindme.database(),
            "Remindme#database([database]) fails to get database of remindme")

    def test_database_sets_database(self):
        self.db = RemindmeDatabase("./test/_test.Remindme.new.db")
        self.remindme.database(self.db)
        self.assertEqual(self.db, self.remindme.database(),
            "Remindme#database([database]) fails to set database of remindme")

    def test_props_gets_props(self):
        self.assertTrue(isinstance(self.remindme.props(), dict),
            "Remindme#props() gets props not in a dictionary")

    @unittest.skip("not written yet")
    def test_save_saves_into_database(self):
        pass

    @unittest.skip("not written yet")
    def test_delete_deletes_from_database(self):
        pass
