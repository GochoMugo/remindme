#! /usr/bin/python3.2

'''
Unit Testing for RemindMe
~~~~~~~~~~~~~~~~~~~~
Main Objectives:
----------------
1. Being able to recover if data is corrupted
2. Handling missing storage file
'''
import os
import unittest
from remindme import remindme


class RemindMeTests(unittest.TestCase):

    def setUp(self):
        remindme.storage_file = os.path.join(os.getcwd(), '.test_remindme')
        self.sample_list = [
            {'keyword': 'python', 'content': 'so good'},
            {'keyword': 'coffee script', 'content': 'that too'},
            {'keyword': 'c', 'content': 'makes me sweaty'},
            {'keywoord': 'corrupted1', 'content': 'corrupted entry'},
            {'keyword': 'corrupted2', 'conteent': 'corrupted entry'}
        ]

    def tearDown(self):
        if os.path.exists(remindme.storage_file):
            os.remove(remindme.storage_file)

    def test_reading(self):
        if os.path.exists(remindme.storage_file):
            os.remove(remindme.storage_file)
        content = remindme.read()
        self.assertEqual(content, [], 'Handling non-existing storage file')

    def test_writing(self):
        wrote = remindme.write(self.sample_list)
        self.assertTrue(wrote, 'Writing to file')

    def test_searching(self):
        search = remindme.search(self.sample_list, 'python')
        result = self.sample_list[0]['content']
        self.assertEqual(search, result, 'Searching for an existing keyword')
        search = remindme.search(self.sample_list, 'ruby')
        self.assertFalse(search, 'Searching for missing keyword')
        search = remindme.search(self.sample_list, 'corrupted2')
        result = 'ReadMe: Content is Corrupted'
        self.assertEqual(search, result, 'Searching for Corrupted Content')

    def test_adding(self):
        added = remindme.add(self.sample_list, 'remind', 'i don\'t remember')
        self.assertTrue(added, 'Adding new remindmes')

    def test_removing_key(self):
        removal = remindme.remove(self.sample_list, 'python')
        self.assertTrue(removal, 'Removing existing remindmes')
        removal = remindme.remove(self.sample_list, 'ruby')
        self.assertFalse(removal, 'Removing non-existing remindmes')


if __name__ == '__main__':
    unittest.main()
