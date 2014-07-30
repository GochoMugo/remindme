'''
The Core of RemindMe
~~~~~~~~~~~~~~~~~
Implemented as pythonic as possible

Copyright (c) 2014 GOCHO MUGO I.
'''

import argparse
import colorama
import os
import sqlite3
import sys

__version__ = '0.1.0'
home = os.path.expanduser('~')
db_file = os.path.join(home, '.remindme.db')
_default = colorama.Fore.WHITE
_error = colorama.Fore.RED
_priority = colorama.Fore.MAGENTA
_reset = colorama.Style.RESET_ALL
_success = colorama.Fore.GREEN


def read(db_file=db_file):
    content = []
    with sqlite3.connect(db_file) as db:
        cursor = db.cursor()
        try:
            sql = 'SELECT keyword, content FROM remindmes'
            for item in cursor.execute(sql).fetchall():
                content.append(item)
        except sqlite3.OperationalError:
            try:
                sql = 'CREATE TABLE remindmes(keyword, content)'
                cursor.execute(sql)
                sql = 'CREATE UNIQUE INDEX keys ON remindmes(keyword)'
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
    return content


def write(keyword, content, db_file=db_file):
    with sqlite3.connect(db_file) as db:
        try:
            cursor = db.cursor()
            sql = 'INSERT INTO remindmes VALUES (?,?)'
            cursor.execute(sql, (keyword, content,))
            db.commit()
            return True
        except:
            db.rollback()
            return True
    return False


def search(content, keyword):
    for item in content:
        if item[0] == keyword:
            return item[1]
    return False


def add(content, keyword, new_content, db_file=db_file):
    if not search(content, keyword):
        return write(keyword, new_content, db_file)
    return False


def remove(content, keyword, db_file=db_file):
    if search(content, keyword):
        try:
            with sqlite3.connect(db_file) as db:
                sql = 'DELETE FROM remindmes WHERE keyword == "{0}"'
                sql = sql.format(keyword)
                db.execute(sql)
                db.commit()
                return True
        except:
            db.rollback()
            return False
    else:
        return False


def arg_parser():
    parser = argparse.ArgumentParser(
        description='Reminds you of something you knew before',
    )
    parser.add_argument('keywords',
                        metavar='KEYWORDS', nargs='*',
                        help='Keyword to remind me something I knew')
    parser.add_argument('-l', '--list',
                        action='store_true',
                        help='list all RemindMe keywords')
    parser.add_argument('-a', '--add',
                        metavar='keywords',
                        dest='add', nargs='+',
                        help='add new RemindMe')
    parser.add_argument('-r', '--remove',
                        metavar='keywords',
                        dest='remove', nargs='+',
                        help='remove a RemindMe')
    parser.add_argument('-ra', '--remove-all',
                        action='store_true',
                        help='remove all RemindMes')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s {0}'.format(__version__))

    args = parser.parse_args()
    args = vars(args)
    return args


def print_out(_status, content):
    words = '{0}\n{1}\n{2}'
    print(words.format(_status, content, _reset))


def run():
    args = arg_parser()
    content = read()

    if args['list']:
        print_out(_success, 'Found {0} remindme keywords\b'.format(
            len(content))
        )
        keywords = [item[0] for item in content]
        keywords.sort()
        print_out(_default, '\n'.join(keywords))
        return

    if args['add']:
        keyword = ' '.join(args['add'])

        user_input = []
        def get_input():
            if sys.version_info.major < 3:
                return raw_input('> ')
            else:
                return input('> ') 
        print('Enter what you remember now:\n{0}'.format(_default))
        while 1:
            try:
                words = get_input()
                if words == ':end':
                    break
                user_input.append(words)
            except KeyboardInterrupt:
                break
        new_content = '\n'.join(user_input)

        if add(content, keyword, new_content):
            print_out(_success, 'RemindMe will remind you next time')
        else:
            print_out(_error, 'RemindMe failed to get that in memory.\n\
Maybe there is already another RemindMe with the same keyword.')

    if args['remove']:
        keyword = ' '.join(args['remove'])
        if remove(content, keyword):
            print_out(_success, 'RemindMe content successfully removed')
        else:
            print_out(_error, 'RemindMe can NOT remove that. Check if \
the keywords really exist with me.')

    if args['remove_all']:
        keywords = [i[0] for i in content]
        for keyword in keywords:
            if remove(content, keyword):
                print_out(_success, 'Remindme removed: {0}'.format(keyword))
            else:
                print_out(_error, 'Remindme failed to remove: {0}'.format(keyword))

    if args['keywords']:
        keyword = ' '.join(args['keywords'])
        results = search(content, keyword)
        if results:
            print_out(_success, 'RemindMe Reminding you:')
            print_out(_default, results)
        else:
            print_out(_error, 'RemindMe: I too can\'t rember that')

if __name__ == '__main__':
    run()
