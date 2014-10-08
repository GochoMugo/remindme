#!/usr/bin/env python
'''
Unit Testing for RemindMe
~~~~~~~~~~~~~~~~~~~~
'''

import os
import subprocess
import sys
import unittest
from remindme import remindme
from remindme import db


class RemindMeTests(unittest.TestCase):

    def setUp(self):
        self.storage_file = os.path.join(os.getcwd(), '.test_db')
        self.sample_list = [
            ('python', 'so good'),
            ('coffee script', 'that too'),
            ('c', 'makes me sweaty'),
        ]

    def tearDown(self):
        if os.path.exists(self.storage_file):
            os.remove(self.storage_file)

    def test_db_reading(self):
        if os.path.exists(self.storage_file):
            os.remove(self.storage_file)
        content = db.read(self.storage_file)
        self.assertEqual(content, [], 'Handling non-existing storage file')

    def test_db_writing(self):
        for item in self.sample_list:
            wrote = db.write(item[0], item[1], db_file=self.storage_file)
            self.assertTrue(wrote, 'Writing to file')

    def test_db_searching(self):
        result = db.search(self.sample_list, 'python')
        expected = 'so good'
        self.assertEqual(result, expected, 'Searching for an existing keyword')
        result = db.search(self.sample_list, 'ruby')
        self.assertFalse(result, 'Searching for missing keyword')

    def test_db_adding(self):
        result = db.add(self.sample_list, 'javascript',
                              'powerful and simple', self.storage_file)
        self.assertTrue(result, 'Adding new remindmes')
        result = db.add(self.sample_list, 'python',
                              'i love it', self.storage_file)
        self.assertFalse(result, 'Adding existing remindmes')

    def test_removing(self):
        removal = db.remove(self.sample_list, 'python')
        self.assertTrue(removal, 'Removing existing remindmes')
        removal = db.remove(self.sample_list, 'ruby')
        self.assertFalse(removal, 'Removing non-existing remindmes')

    def test_piping_in(self):
        keyword = 'FGRYG'
        content = 'REMINDME'
        pipe_in_command = "echo {0}".format(content)
        base = "python -c 'import remindme; remindme.run()' "
        command = "{0} -i {1}".format(base, keyword)
        read_command = "{0} {1}".format(base, keyword)
        clean_up_command = "{0} -r {1}".format(base, keyword)
        subprocess.check_call(
            ' | '.join([pipe_in_command, command]),
            shell=True)
        with open(keyword, 'w+') as out:
            result = subprocess.check_call(
                read_command,
                shell=True,
                stdout=out)
            out.seek(0)
            readContent = out.read()
            self.assertTrue(content in readContent, 'Piping in a remindme')
        # Cleaning up
        subprocess.check_call(clean_up_command, shell=True)
        os.remove('./{0}'.format(keyword))
        sys.stdout.flush()


if __name__ == '__main__':
    unittest.main()
