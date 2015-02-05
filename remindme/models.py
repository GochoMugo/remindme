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
        self.__props = {}
        self.__props["deleted"] = False

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

    def database(self, db=None):
        '''Set or return database reference for the remindme.'''
        if db is None:
            return self.__db
        self.__db = db
        return self

    def props(self):
        '''Return properties of the remindme.'''
        return self.__props

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
            self.__props["deleted"] = True
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
        try:
            remindme.save()
            self.__remindmes.append(remindme)
            return remindme
        except:
            return None

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

    def __filter_out(self, func):
        self.__remindmes = [r for r in self.__remindmes
            if r.props()["deleted"] is False]
        return func()

    @self.__filter_out
    def get_remindmes(self):
        '''Return remindmes from database.'''
        return self.__remindmes

    @self.__filter_out
    def save_remindmes(self):
        '''Save all remindmes.'''
        for remindme in self.__remindmes:
            remindme.save()

    @self.__filter_out
    def find(self, qualify):
        '''Search through the remindmes.'''
        return [x for x in self.__remindmes if qualify(x)]

    def find_by_title(self, title):
        '''Find the remindme by title'''
        return self.find(lambda remindme: remindme.title() == title)

    def remove(self, qualify):
        '''Remove a remindme from database.'''
        remindme = self.find(qualify)
        remindme.delete()
        return remindme
