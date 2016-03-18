import os
import sys
import colorama
from . import metadata


# project metadata
METADATA = metadata


# paths
PATHS = {}
PATHS["home"] = os.path.expanduser("~")
PATHS["db_file"] = os.path.join(PATHS["home"], ".remindme.db")
PATHS["config_file"] = os.path.join(PATHS["home"], ".remindme")


# colors
colorama.init()
COLORS = {}
COLORS["default"] = colorama.Fore.WHITE
COLORS["error"] = colorama.Fore.RED
COLORS["info"] = colorama.Fore.MAGENTA
COLORS["reset"] = colorama.Style.RESET_ALL
COLORS["success"] = colorama.Fore.GREEN


# python version
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


# cryptography settings
CRYPTO = {}
CRYPTO["kdf_iterations"] = 100000
CRYPTO["kdf_length"] = 32

# default user settings
USER_SETTINGS = {}
USER_SETTINGS["disable_encryption"] = False
USER_SETTINGS["encrypt_by_default"] = True
USER_SETTINGS["retry_password_match"] = True
USER_SETTINGS["retry_decryption"] = False
USER_SETTINGS["end_line"] = ":end"
