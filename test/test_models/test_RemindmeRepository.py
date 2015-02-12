'''
Testing RemindmeRepository model.

Objectives:
 - ensure a consistent interface is maintained
'''

import unittest
from remindme.models import Remindme, RemindmeRepository


class Test_RemindmeRepository_Model(unittest.TestCase):
    '''Tests against the RemindmeRepository model
    (remindme.models.RemindmeRepository).'''

    def setUp(self):
        self.db_file = "./test/_test.RemindmeRepository.db"
        self.repository = RemindmeRepository(self.db_file)
        self.data = [
            { "title": "my title is awesome", "content": "and so is my content" },
            { "title": "boring but real title", "content": "get some content for me" },
            { "title": "pizza lover", "content": "some good pizza for me" }
        ]
        for d in self.data:
            self.repository.create_remindme(d["title"], d["content"])

    def test_insert_remindme(self):
        title = "gotcha boy"
        content = "pink stars are awesome"
        remindme = Remindme(title, content, self.repository)
        status = self.repository.insert_remindme(remindme)
        self.assertTrue(status,
            '''RemindmeRepository#insert_remindme(remindme) failed to insert
            remindme''')
        found_remindme = self.repository.find_by_title(title)
        self.assertEqual(content, found_remindme.get_content(),
            '''RemindmeRepository#insert_remindme(remindme) failed to insert
            remindme''')

    def test_insert_remindme_with_same_title(self):
        title = "same old title"
        remindme_1 = Remindme(title, "some content", self.repository)
        remindme_2 = Remindme(title, "other content", self.repository)
        status = self.repository.insert_remindme(remindme_1)
        self.assertTrue(status,
            '''Unexpected error with RemindmeRepository#insert_remindme''')
        status = self.repository.insert_remindme(remindme_2)
        self.assertFalse(status,
            '''RemindmeRepository#insert_remindme fails to return False when
            a remindme fails to be inserted''')

    def test_create_remindme(self):
        title = "some good title, boo"
        content = "got some content for you!"
        remindme = self.repository.create_remindme(title, content)
        self.assertTrue(isinstance(remindme, Remindme),
            '''RemindmeRepository#create_remindme(title, content) does NOT
            return an instance of Remindme''')

    def test_remove_remindme(self):
        remindme_to_remove = self.repository.get_remindmes()[0]
        self.repository.remove_remindme(remindme_to_remove)
        remindmes = self.repository.get_remindmes()
        found_remindme = (len([r for r in remindmes
            if r.get_title() == remindme_to_remove.get_title()]) == 0)
        self.assertTrue(found_remindme,
            '''RemindmeRepository#remove_remindme fails to remove remindme''')

    def test_remove_remindmes(self):
        remindmes = self.repository.get_remindmes()
        self.repository.remove_remindmes()
        any_remindmes = self.repository.get_remindmes()
        self.assertEqual([], any_remindmes,
            '''RemindmeRepository#remove_remindmes fails to remove all
            remindmes''')
        for r in remindmes:
            self.repository.insert_remindme(r)
