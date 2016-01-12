'''
A Remindme is an Entity representing a single user-defined remindme.
'''

import base64
import os
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from . import config


class Remindme:
    '''A user's single remindme.'''

    def __init__(self, title, content, password=None, salt=None, repository=None):
        '''Creates new remindme.'''
        self.__title = title
        self.__content = content
        self.__salt = salt or None
        self.__repository = repository
        self.__props = {}
        self.__props["saved"] = False
        self.__props["deleted"] = False
        if password is not None:
            self.set_content(content, password=password)

    def set_title(self, title):
        '''Set title of this remindme.'''
        self.__title = title
        return self

    def get_title(self):
        '''Return title of this remindme.'''
        return self.__title

    def get_salt(self):
        '''Return salt used to encrypt content of this remindme'''
        return self.__salt

    def is_encrypted(self):
        '''Return true if remindme content needs to be decrypted'''
        return True if self.__salt is not None else False

    def set_content(self, content, password=None):
        '''Set content of this remindme.'''
        # when we do not require encryption
        if password is None:
            self.__content = content
            self.__salt = None
        else:
            self.__salt = os.urandom(16)
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), backend=default_backend(), salt=self.__salt,
                             length=config.CRYPTO["kdf_length"], iterations=config.CRYPTO["kdf_iterations"])
            key = base64.urlsafe_b64encode(kdf.derive(bytes(password)))
            fernet = Fernet(key)
            self.__content = fernet.encrypt(bytes(content))
        return self

    def get_content(self, password=None):
        '''Return content of this remindme.'''
        if password is None or self.__salt is None:
            return self.__content
        # we need to decrypt, using the password
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256, backend=default_backend(), salt=self.__salt,
                         length=config.CRYPTO["kdf_length"], iterations=config.CRYPTO["kdf_iterations"])
        key = base64.urlsafe_b64encode(kdf.derive(bytes(password)))
        fernet = Fernet(key)
        try:
            return str(fernet.decrypt(self.__content))
        except cryptography.fernet.InvalidToken:
            return None

    def set_repository(self, repository):
        '''Set repository reference for this remindme.'''
        self.__repository = repository
        return self

    def get_repository(self):
        '''Return repository reference for this remindme.'''
        return self.__repository

    def get_props(self):
        '''Return properties of this remindme.'''
        return self.__props

    def save(self):
        '''Save remindme into repository.'''
        if self.__repository is not None:
            status = self.__repository.insert_remindme(self)
            self.__props["saved"] = status
            return status
        return False

    def set_as_deleted(self):
        self.__props["deleted"] = True

    def delete(self):
        '''Deletes the remindme from repository.'''
        if self.__repository is not None:
            status = self.__repository.remove_remindme(self)
            self.__props["deleted"] = status
            return status
        return False
