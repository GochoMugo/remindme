'''
Command-line runner for Application
'''

import argparse
import sys
from . import config
from . import utils
from .RemindmeRepository import RemindmeRepository


# start-up activities
console = utils.Console("runner")
gui = utils.GUI()
repository = RemindmeRepository(config.PATHS["db_file"])


def arg_parser():
    '''Argument Parser.'''
    parser = argparse.ArgumentParser(
        description='Reminds you of something you knew before',
        epilog="See LICENSE at {0}".format(config.LICENSE)
    )
    parser.add_argument('keywords',
                        metavar='TITLE', nargs='*',
                        help='title for remindme')
    parser.add_argument('-l', '--list',
                        action='store_true',
                        help='list all remindme titles')
    parser.add_argument('-a', '--add',
                        metavar='title',
                        dest='add', nargs='+',
                        help='add new remindme')
    parser.add_argument('-e', '--edit',
                        metavar='title',
                        dest='edit', nargs='+',
                        help='edit old remindme')
    parser.add_argument('-i', '--in',
                        metavar='title',
                        dest='in', nargs='+',
                        help='pipe-in input for a new remindme')
    parser.add_argument('-r', '--remove',
                        metavar='title',
                        dest='remove', nargs='+',
                        help='remove a remindme')
    parser.add_argument('-Ra', '--remove-all',
                        action='store_true',
                        help='remove all remindmes')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s {0}'.format(config.__version__))

    args = parser.parse_args()
    args = vars(args)
    return args


def run():
    '''Run the command-line runner.'''
    args = arg_parser()
    settings = utils.Settings.read()

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
            console.error("A remindme already has that title")
            return
        # use editor if available, otherwise use console
        if settings.get("editor", None):
            try:
                content = gui.editor(settings["editor"])
            except Exception as err:
                console.error("External editor (%s) exited with a non-zero status code" % (settings["editor"]))
                console.error(str(err))
                return
        else:
            message = "Enter what you remember now"
            content = console.get_long_input(message)

        if content is "":
            console.error("We have nothing to save!")
            return

        if repository.create_remindme(title, content):
            console.success('Remindme will remind you next time.')
        else:
            console.error('Remindme failed to get that in memory.')
        return

    if args['edit']:
        title = ' '.join(args['edit'])
        remindme = repository.find_by_title(title)
        if not remindme:
            console.error("no such remindme exists")
            return
        # we require an external editor for this
        if not settings.get("editor", None):
            console.error("you need to set an external editor for editing existing remindmes")
            return
        content = gui.editor(settings["editor"], remindme.get_content())
        remindme.set_content(content)
        if repository.update_remindme(remindme):
            console.success('The remindme has been updated.')
        else:
            console.error('Remindme failed to save the remindme.')
        return

    if args['in']:
        title = ' '.join(args['in'])
        content = sys.stdin.read().strip()
        if content is '':
            console.error('Remindme got no data!')
        else:
            if repository.create_remindme(title, content):
                console.success('Remindme will remind you next time')
            else:
                console.error('Remindme failed to get that in memory.\n\
Maybe there is already another remindme with the same title.')

    if args['remove']:
        title = ' '.join(args['remove'])
        remindme = repository.find_by_title(title)
        if remindme and remindme.delete():
            console.success('remindme successfully removed')
        else:
            console.error('Remindme can not remove that. Check if the remindme \
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
