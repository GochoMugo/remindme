import sys
from . import config


class console:
    template_log = "[{title}]: {color}{message}" + config.COLORS["reset"]

    def __init__(self, title):
        self.template = template_log.format(title=title)

    def __write(self, _message, color_code, newline):
        message = self.template.format(color=config.COLORS[color_code])
        message = self.template.format(message=_message)
        message += "\n" if newline is True else ""
        sys.stdout.write(message)
        sys.stdout.flush()

    def log(self, message, newline=True):
        self.__write(message, "", newline)
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
