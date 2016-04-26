# -*- coding: utf-8 -*-
"""
@author: adam@wisehippy.co>
"""

import sys



try:
    import MySQLdb
    import MySQLdb.cursors
except ImportError:
    print "Install MySQLdb to continue"
    sys.exit(2)

try:
    from sp.base import Exceptions
except:
    print "Install sp into sys.path()"
    sys.exit(2)




class Connect(object):

    def __init__(self, host, port, user, password, db, cursorclass="dict"):
        """
        Class to use to connect to Mysql database.  Must specify host, port,
        user, password and database.  Default cursor is dict unless otherwise
        specified.
        """
        self.host = host

        try:
            self.port = int(port)
        except ValueError, e:
            raise Exceptions.DatabaseConnectError(e)
        
        #TODO: validate input
        self.user = user
        self.password = password
        self.db = db
        self.cursorclass = cursorclass
        self.conn = None
        self.cursor = None
        self._connect_to_db(self.host, self.port, self.user,
                            self.password, self.db)


    def _connect_to_db(self, host, port, user, password, db):

        try:
            if self.cursorclass == "dict":
                self.conn = MySQLdb.connect(host=host, port=port, user=user,
                                            passwd=password, db=db,
                                            cursorclass=MySQLdb.cursors.DictCursor)
            else:
                self.conn = MySQLdb.connect(host=host, port=port, user=user,
                                            passwd=password, db=db)

            # Could set cursor here, but going to return new cursors instead with get_cursor()
            # self.cursor = self.conn.cursor()

            return True

        except MySQLdb.Error, e:
            raise Exception(e)
            # return None


    def select_sql(self, cursor, sql, fetch="all"):
        """
        Method to use for SELECT, default is fetch all result sets back,
        otherwise if integer is > 1, then will fetchmany(n), if integer
        is <= 1, then will use fetchone()
        """

        cursor.execute(sql)

        if type(fetch) is int and fetch > 1:
            return cursor.fetchmany(fetch)
        elif type(fetch) is int and fetch <= 1:
            return cursor.fetchone()
        else:
            return cursor.fetchall()


    def insert_sql(self, cursor, sql, rollback=True):
        """
        Method to use for INSERT, default is to rollback transaction (if innodb)
        otherwise ignored
        """
        try:
            cursor.execute(sql)
            self.conn.commit()

            return True
        except Exception, e:
            if rollback:

                try:
                    print "%s: CRITICAL: Rolling back: %s" % (self.__class__, e)
                    
                    self.conn.rollback()

                    return False
                except MySQLdb.NotSupportedError:
                    # Not using InnoDB
                    pass
            else:
                raise Exception(e)


    def update_sql(self, cursor, sql, rollback=True):
        """
        Method to use for UPDATE, default is to rollback transaction (if innodb)
        otherwise ignored
        """
        return self.insert_sql(cursor, sql, rollback)


    def get_cursor(self, cursorclass="dict"):
        """
        Yield new Mysql database cursor to use.  Can override cursor type here
        for a one-time use
        """
        # yield self.conn.cursor() does NOT work
        if cursorclass == self.cursorclass:
            return self.conn.cursor()
        elif cursorclass == "cursor":
            return self.conn.cursor(cursorclass=MySQLdb.cursors.Cursor)
        else:
            return self.conn.cursor()


""" ___EOF___ """
