'''
Command-line runner for Application
'''

import argparse
import sys
from . import config
from . import utils
from .Repository import Repository


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


def main():
    '''Run actions.'''
    settings = utils.Settings()
    console = utils.Console("runner", settings)
    gui = utils.GUI()
    repository = Repository(config.PATHS["db_file"])
    args = arg_parser()
    retry_decryption = settings.get("retry_decryption")
    remindme_title = ' '.join(args['keywords']) or None

    def try_decrypt(remindme):
        if not remindme.is_encrypted():
            return remindme.get_content(), None
        content = None
        password = None
        while 1:
            password = get_password()
            content = remindme.get_content(password=password)
            if content:
                break
            console.error("could not decrypt content")
            # TODO: max retries!
            if retry_decryption:
                continue
            raise utils.DecryptionError("could not decrypt content for remindme '%s'" % (remindme.get_title()))
        return content, password

    def get_password(retry=False):
        # determining whether to ask for a password based on need to encrypt
        encryption_disabled = settings.get("disable_encryption")
        encrypt_by_default = settings.get("encrypt_by_default")
        retry_password = retry and settings.get("retry_password_match")
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
        if repository.find_by_title(remindme_title):
            console.error("A remindme already has that title")
            return 1
        # use editor if available, otherwise use console
        editor_cmd = settings.get("editor")
        if editor_cmd:
            try:
                content = gui.editor(editor_cmd)
            except utils.EditorError:
                console.error("External editor (%s) exited with a non-zero status code" % (editor_cmd))
                return 1
        else:
            message = "Enter what you remember now"
            content = console.get_long_input(message)
        # we need content, we do not create empty remindmes!
        if not content:
            console.error("We have nothing to save!")
            return 1
        # ask for the password to use
        password = get_password(retry=True)
        if not repository.create_remindme(remindme_title, content, password=password):
            console.error('Remindme failed during creation.')
            return 1
        console.success('Remindme will remind you next time.')
        return 0

    if args['edit']:
        remindme = get_remindme(remindme_title)
        if not remindme:
            console.error("no such remindme exists")
            return 1
        # we require an external editor for this
        editor_cmd = settings.get("editor")
        if not editor_cmd:
            console.error("you need to set an external editor for editing existing remindmes")
            return 1
        # editing encrypted content
        content = None
        password = None
        try:
            content, password = try_decrypt(remindme)
            content = gui.editor(editor_cmd, content=content)
        except utils.DecryptionError:
            return 1
        except utils.EditorError:
            console.error("External editor (%s) exited with a non-zero status code" % (editor_cmd))
            return 1
        # update content, only if we got some content
        if not content:
            console.error("No content for update.")
            console.log("Consider removing the remindme instead.")
            return 1
        remindme.set_content(content, password=password)
        if not repository.update_remindme(remindme):
            console.error('Remindme failed to save the remindme.')
            return 1
        console.success('The remindme has been updated.')
        return 0

    if args['in']:
        if repository.find_by_title(remindme_title):
            console.error("A remindme already has that title")
            return 1
        content = sys.stdin.read().strip()
        if content is '':
            console.error('Remindme got no data from stdin')
            return 1
        password = get_password()
        if not repository.create_remindme(remindme_title, content, password=password):
            console.error('Remindme failed to create remindme.')
            return 1
        console.success('Remindme created.')
        return 0

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
        if not remindme:
            console.error("No such remindme exists")
            return 1
        if not remindme.delete():
            console.error("Failed to remove remindme")
            return 1
        console.success('remindme successfully removed')
        return 0

    if args['remove_all']:
        confirm = console.get_input("remove All Remindmes(yes/NO)")
        if confirm is None or confirm.strip().lower() != "yes":
            console.error("removal cancelled")
            return 1
        if not repository.remove_remindmes():
            console.error('failed to remove all')
            return 1
        console.success('removed all of them')
        return 0

    # the fallback action, when only a title of a
    # remindme has been provided.
    if remindme_title:
        remindme = get_remindme(remindme_title)
        if not remindme:
            console.error('I too can\'t remember that')
            return 1
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
        return 0
    return 0


def run():
    '''Execute the process and exit with proper exit code.'''
    sys.exit(main())


if __name__ == '__main__':
    run()
