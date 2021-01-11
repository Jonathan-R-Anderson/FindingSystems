import basc_py4chan

class FourChanConnectionHandler:
    def __init__(self):
        pass

    def getBoards(self):
        return [board.name for board in basc_py4chan.get_all_boards()]

    def getTopics(self, board):
        return basc_py4chan.board(board).get_all_threads(expand=True)
