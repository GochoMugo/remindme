'''
Unit Testing for RemindMe
~~~~~~~~~~~~~~~~~~~~
'''

import os
import unittest
from remindme import remindme


class RemindMeTests(unittest.TestCase):

    def setUp(self):
        self.storage_file = os.path.join(os.getcwd(), '.test_remindme.db')
        self.sample_list = [
            ('python', 'so good'),
            ('coffee script', 'that too'),
            ('c', 'makes me sweaty'),
        ]

    def tearDown(self):
        if os.path.exists(self.storage_file):
            os.remove(self.storage_file)

    def test_reading(self):
        if os.path.exists(self.storage_file):
            os.remove(self.storage_file)
        content = remindme.read(self.storage_file)
        self.assertEqual(content, [], 'Handling non-existing storage file')

    def test_writing(self):
        wrote = remindme.write(self.sample_list, self.storage_file)
        self.assertTrue(wrote, 'Writing to file')

    def test_searching(self):
        result = remindme.search(self.sample_list, 'python')
        expected = 'so good'
        self.assertEqual(result, expected, 'Searching for an existing keyword')
        result = remindme.search(self.sample_list, 'ruby')
        self.assertFalse(result, 'Searching for missing keyword')

    def test_adding(self):
        result = remindme.add(self.sample_list, 'javascript',
                              'powerful and simple', self.storage_file)
        self.assertTrue(result, 'Adding new remindmes')
        result = remindme.add(self.sample_list, 'python',
                              'i love it', self.storage_file)
        self.assertFalse(result, 'Adding existing remindmes')

    def test_removing(self):
        removal = remindme.remove(self.sample_list, 'python')
        self.assertTrue(removal, 'Removing existing remindmes')
        removal = remindme.remove(self.sample_list, 'ruby')
        self.assertFalse(removal, 'Removing non-existing remindmes')


if __name__ == '__main__':
    unittest.main()
