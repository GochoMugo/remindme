'''
Command-line runner for Application
'''

import argparse
import sys
from . import config
from . import models
from . import utils


# start-up activities
console = utils.Console("runner")
repository = models.RemindmeRepository(config.PATHS["db_file"])


def arg_parser():
    '''Argument Parser.'''
    parser = argparse.ArgumentParser(
        description='Reminds you of something you knew before',
        epilog="See LICENSE at {0}".format(config.LICENSE)
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
                        version='%(prog)s {0}'.format(config.__version__))

    args = parser.parse_args()
    args = vars(args)
    return args


def run():
    '''Run the command-line runner.'''
    args = arg_parser()

    if args['list']:
        if args['keywords']:
            # searching using a phrase
            phrase = ' '.join(args['keywords'])
            remindmes = repository.find(lambda r: r.get_title().startswith(phrase))
        else:
            remindmes = repository.get_remindmes()
        titles = [r.get_title() for r in remindmes]
        titles.sort()
        num = len(titles)
        console.success('Found {0} remindmes'.format(num))
        if num == 0:
            return
        number = 0
        display_content = ""
        for title in titles:
          number += 1
          display_content = ''.join([display_content, '%-2d - %s\n' % (number, title)])
        console.raw(display_content)
        return

    if args['add']:
        title = ' '.join(args['add'])
        results = repository.find_by_title(title)
        if results:
            console.error("A Remindme already has that title")
            return
        message = "Enter what you remember now"
        content = console.get_long_input(message)

        if content is "":
            console.error("We have nothing to save!")
            return

        if repository.create_remindme(title, content):
            console.success('RemindMe will remind you next time.')
        else:
            console.error('RemindMe failed to get that in memory.')

    if args['in']:
        title = ' '.join(args['in'])
        content = sys.stdin.read().strip()
        if content is '':
            console.error('RemindMe got no data!')
        else:
            if repository.create_remindme(title, content):
                console.success('RemindMe will remind you next time')
            else:
                console.error('RemindMe failed to get that in memory.\n\
Maybe there is already another RemindMe with the same keyword.')

    if args['remove']:
        title = ' '.join(args['remove'])
        remindme = repository.find_by_title(title)
        if remindme and remindme.delete():
            console.success('remindme successfully removed')
        else:
            console.error('can NOT remove that. Check if the remindme \
really exists with me.')

    if args['remove_all']:
        confirm = console.get_input("remove All Remindmes(yes/NO)")
        if confirm.strip().lower() != "yes":
             return console.error("removal cancelled")
        if repository.remove_remindmes():
            console.success('removed all of them')
        else:
            console.error('failed to remove all')

    if args['keywords']:
        title = ' '.join(args['keywords'])
        remindme = repository.find_by_title(title)
        if remindme:
            console.success('Reminding you:')
            lines = remindme.get_content().split("\n")
            number = 0
            for line in lines:
                number += 1
                console.raw("%-2d %s\n" % (number, line))
        else:
            console.error('I too can\'t remember that')


if __name__ == '__main__':
    run()
