'''
A Remindme is an Entity representing a single user-defined remindme.
'''


class Remindme:
    '''A user's single remindme.'''

    def __init__(self, title, content, repository=None):
        '''Creates new remindme.'''
        self.__title = title
        self.__content = content
        self.__repository = repository
        self.__props = {}
        self.__props["saved"] = False
        self.__props["deleted"] = False

    def set_title(self, title):
        '''Set title of this remindme.'''
        self.__title = title
        return self

    def get_title(self):
        '''Return title of this remindme.'''
        return self.__title

    def set_content(self, content):
        '''Set content of this remindme.'''
        self.__content = content
        return self

    def get_content(self):
        '''Return content of this remindme.'''
        return self.__content

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
