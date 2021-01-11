import datetime, threading

class Logger:
    def __init__(self, databaseconnectionhandler, log=False):
        self.databaseconnectionhandler = databaseconnectionhandler
        self.log = log
    def commit(self, level, _class, method, error):
        date = datetime.datetime.now()
        if self.log:
            #self.databaseconnectionhandler.insertIntoError(level, _class, method, error, date)        
            threading.Thread(target=self.databaseconnectionhandler.insertIntoError, args=(level, _class, method, error, date,)).start()
# 0 not really an error, but print worthy
# 1 error, but has been handled
# 2 unhandled error