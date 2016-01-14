import os
import sys
import colorama


# project metadata
__version__ = "0.5.1"
LICENSE = "https://github.com/GochoMugo/remindme/blob/master/LICENSE"


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
