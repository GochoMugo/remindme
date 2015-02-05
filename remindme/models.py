'''
Data models:

i.  Remindme -- a single remindme
ii. RemindmeDatabase -- a sqlite3 database for remindmes
'''


import sqlite3


class Remindme:
    '''A user's single remindme.'''

    def __init__(self, title, content, db=None):
        '''Creates new remindme.'''
        self.__title = title
        self.__content = content
        self.__db = db
        self.__cursor = db.cursor()

    def title(self, title=None):
        '''Set or return title of the remindme.'''
        if title is None:
            return self.__title
        self.__title = title
        return self

    def content(self, content=None):
        '''Set or return content of the remindme.'''
        if content is None:
            return self.__content
        self.__content = content
        return self

    def db(self, db=None):
        '''Set or return database reference for the remindme.'''
        if db is None:
            return self.__db
        self.__db = db
        return self

    def save(self):
        '''Save remindme into database.'''
        if self.__db is None:
            return self
        try:
            sql = 'INSERT INTO remindmes VALUES (?,?)'
            self.__cursor.execute(sql, (self.__title, self.__content,))
            self.__db.commit()
            return self
        except sqlite3.OperationalError:
            self.__db.rollback()
            raise Exception()

    def delete(self):
        '''Deletes the remindme from database.'''
        try:
            sql = 'DELETE FROM remindmes WHERE keyword == "{0}" '
            sql = sql.format(self.__title)
            self.__cursor.execute(sql)
            self.__db.commit()
            return self
        except:
            self.__db.rollback()
            raise Exception()


class RemindmeDatabase:
    '''Database of Remindmes.'''

    def __init__(self, db_file):
        '''Create a sqlite3 database for remindmes.'''
        self.__db = None
        self.__cursor = None
        self.__remindmes = []
        with sqlite3.connect(db_file) as db:
            self.__db = db
            self.__cursor = db.cursor()
            try:
                sql = 'CREATE TABLE IF NOT EXISTS remindmes(title, content)'
                self.__cursor.execute(sql)
                sql = 'CREATE UNIQUE INDEX indices ON remindmes(title)'
                self.__cursor.execute(sql)
                self.__db.commit()
            except Exception:
                raise Exception()

    def new_remindme(self, title, content):
        '''Create a new remindme in the database.'''
        remindme = Remindme(title, content, self.__db)
        self.__remindmes.append(remindme)
        return remindme

    def load_remindmes(self):
        '''Load remindmes from the database.'''
        try:
            sql = 'SELECT keyword, content FROM remindmes'
            for item in self.__cursor.execute(sql).fetchall():
                remindme = Remindme(item[0], item[1], self.__db)
                self.__remindmes.append(remindme)
        except sqlite3.OperationalError:
            pass
        return self

    def get_remindmes(self):
        '''Return remindmes from database.'''
        return self.__remindmes

    def save_remindmes(self):
        '''Save all remindmes.'''
        for remindme in self.__remindmes:
            remindme.save()

    def find(self, title):
        '''Find the remindme.'''
        for remindme in self.__remindmes:
            if remindme.title() is title:
                return remindme
        return None

