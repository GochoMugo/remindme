'''
Testing Remindme model.

Objectives:
 - ensure a consistent interface is maintained
'''

import unittest
from remindme.Remindme import Remindme
from remindme.RemindmeRepository import RemindmeRepository


class Test_Remindme_Model(unittest.TestCase):
    '''Tests against the Remindme model (remindme.models.Remindme).'''

    def setUp(self):
        self.title = "some title"
        self.content = "some content"
        self.repository = RemindmeRepository("./test/_test.Remindme.db")
        self.remindme = Remindme(self.title, self.content, self.repository)

    def test_constructor_sets_title(self):
        self.assertEqual(self.title, self.remindme.get_title(),
            "constructor fails to set title of remindme")

    def test_constructor_sets_content(self):
        self.assertEqual(self.content, self.remindme.get_content(),
            "constructor fails to set content of remindme")

    def test_constructor_sets_repository(self):
        self.assertEqual(self.repository, self.remindme.get_repository(),
            "constructor fails to set repository of remindme")

    def test_title_gets_title(self):
        self.assertEqual(self.title, self.remindme.get_title(),
            "Remindme#get_title() fails to get title of remindme")

    def test_title_sets_title(self):
        self.title = "new title, dummy!"
        self.remindme.set_title(self.title)
        self.assertEqual(self.title, self.remindme.get_title(),
            "Remindme#set_title([title]) fails to set title of remindme")

    def test_content_gets_content(self):
        self.assertEqual(self.content, self.remindme.get_content(),
            "Remindme#get_content() fails to get content of remindme")

    def test_content_sets_content(self):
        self.content = "new content, dummy!"
        self.remindme.set_content(self.content)
        self.assertEqual(self.content, self.remindme.get_content(),
            "Remindme#set_content(content) fails to set content of remindme")

    def test_database_gets_repository(self):
        self.assertEqual(self.repository, self.remindme.get_repository(),
            "Remindme#get_repository() fails to get repository of remindme")

    def test_database_sets_repository(self):
        self.repository = RemindmeRepository("./test/_test.Remindme.new.db")
        self.remindme.set_repository(self.repository)
        self.assertEqual(self.repository, self.remindme.get_repository(),
            "Remindme#set_repository(repository) fails to set repository of remindme")

    def test_props_gets_props(self):
        self.assertTrue(isinstance(self.remindme.get_props(), dict),
            "Remindme#props() gets props not in a dictionary")

    @unittest.skip("not written yet")
    def test_save_saves_into_database(self):
        pass

    @unittest.skip("not written yet")
    def test_delete_deletes_from_database(self):
        pass
