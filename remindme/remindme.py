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
import sys

__version__ = '0.0.1'
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
    if not search(content, keyword):
        content.append(item)
        return write(content)
    return False


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
                        help='Keyword to remind me something I knew')
    parser.add_argument('-l', '--list',
                        action='store_true',
                        help='list all RemindMe keywords')
    parser.add_argument('-a', '--add',
                        metavar='keywords',
                        dest='add', nargs='+',
                        help='add new RemindMe content')
    parser.add_argument('-r', '--remove',
                        dest='remove', nargs='+',
                        help='remove a RemindMe')
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
        keywords = []
        for item in content:
            if 'keyword' in item:
                keywords.append(item['keyword'])
        keywords.sort()
        print_out(_default, '\n'.join(keywords))
        return

    if args['add']:
        keyword = ' '.join(args['add'])
        prompt = 'Enter what you remember now:\n\n>{0}'.format(_default)
        if sys.version_info.major < 3:
            new_content = raw_input(prompt)
        else:
            new_content = input(prompt)
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
