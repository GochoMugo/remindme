import getpass
import json
import os
import subprocess
import sys
import tempfile
import uuid
from . import config


class Console:
    template = "{color}[{title}]: {message}" + config.COLORS["reset"]

    def __init__(self, title, config={}):
        self.title = title
        self.configure(config)

    def configure(self, config):
        self.config = config

    def raw(self, message):
        sys.stdout.write(message)
        sys.stdout.flush()

    def __write(self, _message, color_code, newline):
        message = Console.template.format(title=self.title,
            color=config.COLORS[color_code], message=_message)
        message += "\n" if newline is True else ""
        self.raw(message)

    def log(self, message, newline=True):
        self.__write(message, "reset", newline)
        return self

    def info(self, message, newline=True):
        self.__write(message, "info", newline)
        return self

    def error(self, message, newline=True):
        self.__write(message, "error", newline)
        return self

    def success(self, message, newline=True):
        self.__write(message, "success", newline)
        return self

    def __input(self):
        if config.PY2:
            return raw_input("> ")
        else:
            return input("> ")

    def get_input(self, question):
        '''Prompt for single-line input from user, using the question.

        Returns the input data if entered.
        Returns None if no data was entered.'''
        self.info(question + "?")
        return self.__input() or None

    def get_long_input(self, question):
        '''Prompt for multi-line input from user, using the question.

        Returns a string, if input was entered.
        Returns None if no data was entered.'''
        self.info(question + "?")
        user_input = []
        while 1:
            try:
                words = self.__input()
                if words == self.config.get("end_line", config.USER_SETTINGS["end_line"]):
                    break
                user_input.append(words)
            except KeyboardInterrupt:
                break
        return '\n'.join(user_input) or None

    def get_password(self, prompt="password (leave blank for NO password): ",
                     prompt2="re-enter password: ", retry=False):
        '''Prompt for password, using prompt as question.

        Input is hidden from view.
        Returns a string.'''
        password = None
        self.info(prompt, newline=False)
        password = getpass.getpass(prompt="") or None
        if retry is True:
            # retry till user enters correct password
            self.info(prompt2, newline=False)
            password2 = getpass.getpass(prompt="") or None
            if password != password2:
                self.error("passwords do not match")
                return self.get_password(prompt=prompt, prompt2=prompt2, retry=retry)
        return password


class GUI:
    def editor(self, editor, content=None):
        '''Opens an external editor for editing. Returns entered
        contents once editor is closed.

        Throws subprocess.CalledProcessError if the editor errors.
        Returns a string, if content could be retrieved.
        Returns None if no content could be retrieved.'''
        filename = ".remindme-" + str(uuid.uuid4())
        filepath = os.path.join(tempfile.gettempdir(), filename)
        # if editing old content, add it to the file before opening an
        # editor to edit the file
        if content:
            with open(filepath, "w") as f:
                f.write(content)
        subprocess.check_call([editor, filepath])
        try:
            with open(filepath) as f:
                content = f.read()
            os.unlink(filepath)
        except:
            # the user might have decided to quit
            # or maybe their editor failed etc.
            # it's up to the callee to react to empty content
            pass
        return content


class Settings:
    config = {}

    @staticmethod
    def read():
        if Settings.config:
            return Settings.config
        if os.path.isfile(config.PATHS["config_file"]):
            with open(config.PATHS["config_file"]) as config_file:
                content = config_file.read()
                content = json.loads(content)
                Settings.config = content
        return Settings.config

    @staticmethod
    def write():
        content = json.dumps(Settings.config, sort_keys=True, indent=4)
        with open(config.PATHS["config_file"], "w") as config_file:
            config_file.write(content)
