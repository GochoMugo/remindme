'''
Command-line runner for Application
'''

import argparse
import sys
from . import config
from . import models
from . import utils


# start-up activities
#console = utils.Console("runner")
#database = models.RemindmeDatabase(config.PATHS["db_file"])


def arg_parser():
    '''Argument Parser.'''
    parser = argparse.ArgumentParser(
        description='Reminds you of something you knew before',
        epilog="See LICENSE at {0}".format(LICENSE)
    )
    parser.add_argument('keywords',
                        metavar='TITLE', nargs='*',
                        help='Title for RemindMe')
    parser.add_argument('-l', '--list',
                        action='store_true',
                        help='list all RemindMe titles')
    parser.add_argument('-a', '--add',
                        metavar='title',
                        dest='add', nargs='+',
                        help='add new RemindMe')
    parser.add_argument('-i', '--in',
                        metavar='title',
                        dest='in', nargs='+',
                        help='pipe-in input for a new remindme')
    parser.add_argument('-r', '--remove',
                        metavar='title',
                        dest='remove', nargs='+',
                        help='remove a RemindMe')
    parser.add_argument('-Ra', '--remove-all',
                        action='store_true',
                        help='remove all RemindMes')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s {0}'.format(__version__))

    args = parser.parse_args()
    args = vars(args)
    return args


def run():
    '''Run the command-line runner.'''
    args = arg_parser()

    if args['list']:
        if args['keywords']:
            # searching using a phrase
            phrase = keyword = ' '.join(args['keywords'])
            keywords = database.find(lambda r: r.title().startswith(phrase))
        else:
            keywords = database.get_remindmes()
        keywords.sort()
        num = len(keywords)
        console.success('Found {0} remindme keywords:'.format(num))
        number = 0
        remindmes = ""
        for i in keywords:
          number += 1
          remindmes = ''.join([remindmes, '%-2d- %s\n' % (number, i)])
        console.log(remindmes)
        return

    if args['add']:
        title = ' '.join(args['add'])
        results = database.find_by_title(title)
        if results:
            console.error("A Remindme already has that title")
            return
        message = "Enter what you remember now"
        content = console.get_long_input(message)

        if user_input is "":
            console.error("We have nothing to save!")
            return

        if database.new_remindme(title, content):
            console.success('RemindMe will remind you next time.')
        else:
            console.error('RemindMe failed to get that in memory.')

    if args['in']:
        title = ' '.join(args['in'])
        content = sys.stdin.read().strip()
        if content is '':
            console.error('RemindMe got no data!')
        else:
            if database.new_remindme(title, content):
                console.success('RemindMe will remind you next time')
            else:
                console.error('RemindMe failed to get that in memory.\n\
Maybe there is already another RemindMe with the same keyword.')

    if args['remove']:
        title = ' '.join(args['remove'])
        if database.remove(lambda r: r.title() == title):
            console.success('remindme successfully removed')
        else:
            console.error('can NOT remove that. Check if the remindme \
really exists with me.')

    if args['remove_all']:
        confirm = console.get_input("remove All Remindmes(yes/NO)")
        if confirm.strip().lower() != "yes":
             return console.error("removal cancelled")
        if database.remove_all():
            console.success('removed all of them')
        else:
            console.error('failed to remove all')

    if args['keywords']:
        title = ' '.join(args['keywords'])
        remindme = database.find_by_title(title)
        if remindme:
            console.success('Reminding you:')
            lines = remindme.content().split("\n")
            number = 0
            for line in lines:
                number += 1
                console.info("%-2d " % (number), newline=False)
                console.log(line)
        else:
            console.error('I too can\'t remember that')


if __name__ == '__main__':
    run()
