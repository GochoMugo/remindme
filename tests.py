'''
Unit Testing for RemindMe
~~~~~~~~~~~~~~~~~~~~
'''

import os
import subprocess
import sys
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

    def test_piping_in(self):
        keyword = 'FGRYG'
        content = 'REMINDME'
        pipe_in_command = "echo {0}".format(content)
        base = "python remindme/remindme.py"
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
