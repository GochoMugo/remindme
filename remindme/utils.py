import json
import os
import subprocess
import sys
import tempfile
import uuid
from . import config


class Console:
    template = "{color}[{title}]: {message}" + config.COLORS["reset"]

    def __init__(self, title):
        self.title = title

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
        self.info(question + "?")
        return self.__input()

    def get_long_input(self, question):
        self.info(question + "?")
        user_input = []
        while 1:
            try:
                words = self.__input()
                if words == ':end':
                    break
                user_input.append(words)
            except KeyboardInterrupt:
                break
        return '\n'.join(user_input)


class GUI:
    def editor(self, editor, content=None):
        '''Opens an external editor for editing. Returns entered
        contents once editor is closed.

        Throws subprocess.CalledProcessError when executing the editor
        executable.'''
        filename = ".remindme-" + str(uuid.uuid4())
        filepath = os.path.join(tempfile.gettempdir(), filename)
        # if editing old content, add it to the file before opening an
        # editor to edit the file
        if content:
            with open(filepath, "w") as f:
                f.write(content)
        subprocess.check_call([editor, filepath])
        with open(filepath) as f:
            content = f.read()
        os.unlink(filepath)
        return content


class Settings:
    config = {}

    @staticmethod
    def read():
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
