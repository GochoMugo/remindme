'''
RemindMe
~~~~~~~~
A Command Line Application that reminds you of somethings you may end
up forgetting. Just add a `remindme` and in the future you could just
make RemindMe show you the content.

Licensed under the MIT License. For Open Source Initiative (OSI)

Contribute to the Project at https://github.com/GochoMugo/remindme
'''

from .config import __version__
from .cli import run


__all__ = ['__version__', 'run', ]
