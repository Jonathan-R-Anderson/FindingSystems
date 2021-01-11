#from FourChan.FourChanConnectionHandler import FourChanConnectionHandler
#from FourChan.BoardScraper import BoardScraper

from FourChanConnectionHandler import FourChanConnectionHandler
from BoardScraper import BoardScraper
import os, sys

class FourChanScraper:
    def __init__(self, fourchanconnectionhandler, databaseconnectionhandler):
        self.fourchanconnectionhandler = fourchanconnectionhandler
        self.databaseconnectionhandler = databaseconnectionhandler

    def getProcessIDS(self):
        pwd = os.getcwd()
        filePath = os.path.join(pwd, "processIDS", "processIDS-fourchan.txt")
        open(filePath, "w+").close()

        with open(filePath, "w+") as f:
            f.write(str(os.getpid()))

    def driver(self):
        # get all boards
        self.getProcessIDS()
        #boards = self.fourchanconnectionhandler.getBoards()
        #boards = ['n', 'v', 'vg', 'vr', 'g', 'tv', 'k', 'o', 'sp', 'sci', 'his', 'int', 'toy', 'fa', 'biz', 'trv', 'news', 'b', 'pol', 'bant', 'r9k']
        boards = ['pol']
        board_threads = []
        for board in boards:
            tmp_fourchanconnectionhandler = FourChanConnectionHandler()
            boardscraper_thread = BoardScraper(tmp_fourchanconnectionhandler, board, self.databaseconnectionhandler)
            board_threads.append(boardscraper_thread)
        for board_thread in board_threads:
            board_thread.start()
