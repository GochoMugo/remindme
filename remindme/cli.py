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
        epilog="See LICENSE at {0}".format(config.METADATA.LICENSE)
    )
    parser.add_argument('keywords',
                        metavar='TITLE', nargs='*',
                        help='title for remindme')
    parser.add_argument('-l', '--list',
                        action='store_true',
                        help='list all remindme titles')
    parser.add_argument('-a', '--add',
                        action='store_true',
                        help='add new remindme')
    parser.add_argument('-e', '--edit',
                        action='store_true',
                        help='edit old remindme')
    parser.add_argument('-i', '--in',
                        action='store_true',
                        help='pipe-in input for a new remindme')
    parser.add_argument('-o', '--raw',
                        action='store_true',
                        help='provide unformatted output; suitable for piping')
    parser.add_argument('-b', '--rename',
                        metavar='new_title', nargs='+',
                        help='rename a remindme')
    parser.add_argument('-r', '--remove',
                        action='store_true',
                        help='remove a remindme')
    parser.add_argument('-Ra', '--remove-all',
                        action='store_true',
                        help='remove all remindmes')
    parser.add_argument('-x', '--encrypt',
                        action='store_true',
                        help='encrypt before storing')
    parser.add_argument('-p', '--plain',
                        action='store_true',
                        help='store as plain text')
    parser.add_argument('-n', '--index',
                        action='store_true',
                        help='use title as index in list')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s {0}'.format(config.METADATA.__version__))

    args = parser.parse_args()
    args = vars(args)
    return args


def run():
    '''Run the command-line runner.'''
    args = arg_parser()
    settings = utils.Settings.read()
    console.configure(settings)
    retry_decryption = settings.get("retry_decryption", config.USER_SETTINGS["retry_decryption"])
    remindme_title = ' '.join(args['keywords']) or None

    def try_decrypt(remindme):
        if not remindme.is_encrypted():
            return remindme.get_content(), None

        content = None
        while 1:
            password = None
            try:
                password = get_password()
            except KeyboardInterrupt:
                return content, None
            content = remindme.get_content(password=password)
            if content is None:
                console.error("could not decrypt text")
            else:
                return content, password
            if retry_decryption is False:
                return content, None

    def get_password(retry=False):
        # determining whether to ask for a password based on need to encrypt
        encryption_disabled = settings.get("disable_encryption", config.USER_SETTINGS["disable_encryption"])
        encrypt_by_default = settings.get("encrypt_by_default", config.USER_SETTINGS["encrypt_by_default"])
        retry_password = retry and settings.get("retry_password_match", config.USER_SETTINGS["retry_password_match"])
        encryption_requested = args["encrypt"] or False
        plaintext_requested = args["plain"] or False
        password = None

        # ensure encryption is not disabled
        if encryption_disabled:
            console.info("encryption is disabled")
            return password

        # if encryption has been requested
        if encryption_requested:
            password = console.get_password(retry=retry_password)
        # if encryption is by default and plaintext has not been requested
        elif encrypt_by_default and not plaintext_requested:
            password = console.get_password(retry=retry_password)

        # warn the user that no password was captured, if the case is so
        if password is None:
            console.info("NO password was captured. Storing as plain text.")

        return password

    def get_remindme(title):
        if args['index']:
            try:
                return repository.find_at_index(title)
            except ValueError:
                console.error("index provided is not an integer")
                return None
        else:
            return repository.find_by_title(title)

    if args['list']:
        if remindme_title:
            remindmes = repository.find(lambda r: r.get_title().startswith(remindme_title))
        else:
            remindmes = repository.get_remindmes()
        titles = repository.titles_in_order(remindmes)
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

    # from here on, we require that the keywords have
    # been provided. Otherwise, exit early
    if not remindme_title:
        console.error("Title of remindme has not been provided")
        return 1

    if args['add']:
        results = repository.find_by_title(remindme_title)
        if results:
            console.error("A remindme already has that title")
            return 1
        # use editor if available, otherwise use console
        if settings.get("editor", None):
            try:
                content = gui.editor(settings["editor"])
            except Exception as err:
                console.error("External editor (%s) exited with a non-zero status code" % (settings["editor"]))
                console.error(str(err))
                return 1
        else:
            message = "Enter what you remember now"
            content = console.get_long_input(message)

        if not content:
            console.error("We have nothing to save!")
            return

        password = get_password(retry=True)
        if repository.create_remindme(remindme_title, content, password=password):
            console.success('Remindme will remind you next time.')
        else:
            console.error('Remindme failed to get that in memory.')
        return

    if args['edit']:
        remindme = get_remindme(remindme_title)
        if not remindme:
            console.error("no such remindme exists")
            return
        # we require an external editor for this
        if not settings.get("editor", None):
            console.error("you need to set an external editor for editing existing remindmes")
            return
        # editing encrypted content
        content, password = try_decrypt(remindme)
        if content is None:
            return 1
        content = gui.editor(settings["editor"], content=content)
        # update content, only if we got some content
        if content:
            remindme.set_content(content, password=password)
        if repository.update_remindme(remindme):
            console.success('The remindme has been updated.')
        else:
            console.error('Remindme failed to save the remindme.')
        return

    if args['in']:
        content = sys.stdin.read().strip()
        if content is '':
            console.error('Remindme got no data!')
        else:
            password = get_password()
            if repository.create_remindme(remindme_title, content, password=password):
                console.success('Remindme will remind you next time')
            else:
                console.error('Remindme failed to get that in memory.\n\
Maybe there is already another remindme with the same title.')
        return

    if args['rename']:
        new_title = ' '.join(args['rename'])
        remindme = get_remindme(remindme_title)
        if not remindme:
            console.error('No such remindme to rename')
            return 1
        if not remindme.set_title(new_title):
            console.error('Remindme could not be renamed')
            return 1
        console.success('Remindme renamed successfully')
        return 0

    if args['remove']:
        remindme = get_remindme(remindme_title)
        if remindme and remindme.delete():
            console.success('remindme successfully removed')
        else:
            console.error('Remindme can not remove that. Check if the remindme \
really exists with me.')
        return

    if args['remove_all']:
        confirm = console.get_input("remove All Remindmes(yes/NO)")
        if confirm is None or confirm.strip().lower() != "yes":
             return console.error("removal cancelled")
        if repository.remove_remindmes():
            console.success('removed all of them')
        else:
            console.error('failed to remove all')
        return

    # the fallback action, when only a title of a
    # remindme has been provided.
    if remindme_title:
        remindme = get_remindme(remindme_title)
        if remindme:
            content, __ = try_decrypt(remindme)
            if content is None:
                console.error('empty remindme content')
                return 1
            # if we are to spit out unmodified content
            if args['raw']:
                console.raw(content)
                return 0
            console.success('Reminding you:')
            lines = content.split("\n")
            number = 0
            for line in lines:
                number += 1
                console.raw("%-2d %s\n" % (number, line))
        else:
            console.error('I too can\'t remember that')
    return 0

if __name__ == '__main__':
    sys.exit(run())
