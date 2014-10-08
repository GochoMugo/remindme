'''
The Core of RemindMe
~~~~~~~~~~~~~~~~~~~~
Implemented as pythonic as possible

Copyright (c) 2014 GOCHO MUGO I.
'''

import argparse
import colorama
import getpass
import sys
import db

__version__ = '0.2.0'
LICENSE = "https://github.com/GochoMugo/remindme/blob/master/LICENSE"
_default = colorama.Fore.WHITE
_error = colorama.Fore.RED
_priority = colorama.Fore.MAGENTA
_reset = colorama.Style.RESET_ALL
_success = colorama.Fore.GREEN
PY2 = sys.version_info.major == 2
PY3 = sys.version_info.major == 3


def arg_parser():
    parser = argparse.ArgumentParser(
        description='Reminds you of something you knew before',
        epilog="See LICENSE at {0}".format(LICENSE)
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
    parser.add_argument('-i', '--in',
                        metavar='keywords',
                        dest='in', nargs='+',
                        help='pipe-in input for a new remindme')
    parser.add_argument('-r', '--remove',
                        metavar='keywords',
                        dest='remove', nargs='+',
                        help='remove a RemindMe')
    parser.add_argument('-Ra', '--remove-all',
                        action='store_true',
                        help='remove all RemindMes')
    parser.add_argument('-k', '--key',
                        action='store_true',
                        help='Enable/Disable key')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s {0}'.format(__version__))

    args = parser.parse_args()
    args = vars(args)
    return args


def print_out(_status, content, newline=True):
    words = '{0}{1}{2}'
    words += "\n" if newline is True else ""
    sys.stdout.write(words.format(_status, content, _reset))
    sys.stdout.flush()


def get_input(question=""):
    if PY2:
        return raw_input(question + '> ')
    else:
        return input(question + '> ')


def run():
    args = arg_parser()
    content = db.read()

    if args['list']:
        keywords = [item[0] for item in content]
        if args['keywords']:
            # searching using a phrase
            phrase = keyword = ' '.join(args['keywords'])
            keywords = [i for i in keywords if i.startswith(phrase)]
        keywords.sort()
        num = len(keywords)
        print_out(_success if num > 0 else _error,
              'Found {0} remindme keywords:'.format(num)
        )
        number = 0
        remindmes = ""
        for i in keywords:
          number += 1
          remindmes = ''.join([remindmes, '%-2d- %s\n' % (number, i)])
        print_out(_default, remindmes)
        return

    if args['add']:
        keyword = ' '.join(args['add'])
        results = db.search(content, keyword)
        if results:
            print_out(_error, "A Remindme already has that name")
            return
        user_input = []
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

        if db.add(content, keyword, new_content):
            print_out(_success, 'RemindMe will remind you next time')
        else:
            print_out(_error, 'RemindMe failed to get that in memory.')

    if args['in']:
        keyword = ' '.join(args['in'])
        new_content = sys.stdin.read().strip()
        if new_content == '':
            print_out(_error, 'RemindMe got no data')
        else:
            if db.add(content, keyword, new_content):
                print_out(_success, 'RemindMe will remind you next time')
            else:
                print_out(_error, 'RemindMe failed to get that in memory.\n\
Maybe there is already another RemindMe with the same keyword.')

    if args['remove']:
        keyword = ' '.join(args['remove'])
        if db.remove(content, keyword):
            print_out(_success, 'RemindMe content successfully removed')
        else:
            print_out(_error, 'RemindMe can NOT remove that. Check if \
the keywords really exist with me.')

    if args['remove_all']:
        confirm = get_input("Remove All Remindmes(yes/NO)")
        if confirm.strip().lower() != "yes":
             return print_out(_error, "Removal cancelled")
        keywords = [i[0] for i in content]
        for keyword in keywords:
            if db.remove(content, keyword):
                print_out(_success,
                          'Remindme removed: {0}'.format(keyword))
            else:
                print_out(_error,
                          'Remindme failed to remove: {0}'.format(keyword))

    if args['key']:
        print_out(_error, 'Not implemented yet')

    if args['keywords']:
        keyword = ' '.join(args['keywords'])
        results = db.search(content, keyword)
        if results:
            print_out(_success, 'RemindMe Reminding you:')
            results = results.split("\n")
            number = 0
            for line in results:
                number += 1
                print_out(_priority, "%-2d " % (number), newline=False)
                print_out(_default, line)
        else:
            print_out(_error, 'RemindMe: I too can\'t remember that')


if __name__ == '__main__':
    run()
