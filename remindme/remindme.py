'''
The Core of RemindMe
~~~~~~~~~~~~~~~~~
Implemented as pythonic as possible

Copyright (c) 2014 GOCHO MUGO I.
'''

import argparse
import colorama
import json
import os

__version__ = '0.0.0'
home = os.path.expanduser('~')
storage_file = os.path.join(home, '.remindme')
_default = colorama.Fore.WHITE
_error = colorama.Fore.RED
_priority = colorama.Fore.MAGENTA
_reset = colorama.Style.RESET_ALL
_success = colorama.Fore.GREEN


def read():
    try:
        with open(storage_file, 'r') as storage:
            content = storage.read()
            content = json.loads(content)
            return content
    except IOError:
        with open(storage_file, 'w') as storage:
                content = json.dumps([])
                content = storage.write(content)
                return []


def write(content):
    with open(storage_file, 'w') as storage:
        content.sort()
        content = json.dumps(content, indent=4)
        storage.write(content)
        return True
    return False


def search(content, keyword):
    for item in content:
        if 'keyword' in item:
            if keyword in item['keyword']:
                if 'content' in item:
                    return item['content']
                return 'ReadMe: Content is Corrupted'
    return False


def add(content, keyword, new_content):
    item = {
        'keyword': keyword,
        'content': new_content
    }
    content.append(item)
    return write(content)


def remove(content, keyword):
    if search(content, keyword):
        newContent = []
        for item in content:
            if 'keyword' in item:
                if item['keyword'] != keyword:
                    newContent.append(item)
        return write(content)
    return False


def arg_parser():
    parser = argparse.ArgumentParser(
        description='Reminds you of something you knew before',
    )
    parser.add_argument('keywords',
                        metavar='KEYWORDS', nargs='*',
                        help='Remindme something I knew')
    parser.add_argument('-l', '--list',
                        action='store_true',
                        help='List all remindme keywords')
    parser.add_argument('-a', '--add',
                        metavar='keywords',
                        dest='add', nargs='+',
                        help='Add new remindme content')
    parser.add_argument('-r', '--remove',
                        dest='remove', nargs='+',
                        help='Remove a remindme')
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
        print_out(_success, 'Found {0} remindme keywords'.format(
            len(content))
        )
        for item in content:
            print(item['keyword'])
        return

    if args['add']:
        keyword = ' '.join(args['add'])
        new_content = raw_input('Enter what you remember now:\n')
        if add(content, keyword, new_content):
            print_out(_success, 'RemindMe will remind you next time')
        else:
            print_out(_error, 'RemindMe failed to get that in memory')

    if args['remove']:
        keyword = ' '.join(args['remove'])
        if remove(content, keyword):
            print_out(_success, 'RemindMe content successfully removed')
        else:
            print_out(_error, 'RemindMe can NOT remove that. Check if \
the keywords really exist with me.')

    if args['keywords']:
        keyword = ' '.join(args['keywords'])
        results = search(content, keyword)
        if results:
            print_out(_success, 'RemindMe Reminding you:\n')
            print_out(_default, results)
        else:
            print_out(_error, 'RemindMe: I too can\'t rember that')

if __name__ == '__main__':
    run()
