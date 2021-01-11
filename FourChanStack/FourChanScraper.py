import os

class Topic:
    def __init__(self, topic):
        self.topic = topic
        self.replies = []
        self.final_dictionary = {} # {Date: [ sentences are here, this is a second sentence, okay ]}
        self.isDead = False

class Board:
    def __init__(self, board, fourchanconnectionhandler, databaseconnectionhandler):
        self.board = board
        self.fourchanconnectionhandler = fourchanconnectionhandler
        self.databaseconnectionhandler = databaseconnectionhandler
        self.live_topics = []
        # get all new topics
        new_topics = [topic for topic in self.fourchanconnectionhandler.getTopics(self.board)]
        # add new topics to stack
        for topic in new_topics:
            tmp_topic = Topic(topic)
            self.live_topics.append(tmp_topic)       

    def processPosts(self, topic):
        if (not topic.topic.sticky and not topic.topic.is_404 and not topic.topic.closed and not topic.topic.archived):
            if (topic.topic.update() > 0):
                new_replies =  [reply for reply in topic.topic.all_posts if reply.post_id not in topic.topic.replies]
                for reply in new_replies:
                    topic.replies.append(reply.post_id)
                    #print("Adding reply", reply.post_id)
                    reply_date = int(reply.datetime.timestamp())
                    if (reply_date not in topic.final_dictionary.keys()):
                        topic.final_dictionary[reply_date] = [reply.comment.lower()] # create new entry for a comment at the specified date in the dictionary
                    else:
                        topic.final_dictionary[reply_date].append(reply.comment.lower()) # if entry for a comment's date already exists, append the comment to an array
        else:
            for date in topic.final_dictionary.keys():
                database_date = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S') # formatting the date for the database
                for comment in topic.final_dictionary[date]: # iterate through all comments for a specific datetime
                    def striphtml(data):
                        p = re.compile(r'<.*?>|&gt|gt') # regular expression to strip out special characters at the beginning of the comment
                        return p.sub('', data)
                    comment = striphtml(comment)
                    print("Adding comment", comment)
                    self.databaseconnectionhandler.insertWordIntowordcount("4chan", {database_date : comment}) # commit the data to the database
            topic.isDead = True

    def processTopics(self):
        new_topics = []
        for topic in self.live_topics:
            # get all new topics
            tmp_new_topics = [topic for topic in self.fourchanconnectionhandler.getTopics(self.board) if topic.id not in [topic.topic.id for topic in self.live_topics]]
            # add new topics to stack
            for new_topic in tmp_new_topics:
                #print("Adding topic", new_topic)
                tmp_topic = Topic(new_topic)
                new_topics.append(tmp_topic)
            # process current posts
            print("Processing topic", topic.topic.id)
            self.processPosts(topic)
        [self.live_topics.append(topic) for topic in new_topics]
        [self.live_topics.remove(topic) for topic in self.live_topics if topic.isDead]

class FourChanScraper:
    def __init__(self, fourchanconnectionhandler, databaseconnectionhandler):
        self.fourchanconnectionhandler = fourchanconnectionhandler
        self.databaseconnectionhandler = databaseconnectionhandler

    def getProcessIDS(self):
        pwd = os.getcwd()
        filePath = os.path.join(pwd, "processIDS", "processIDS-fourchanstack.txt")
        open(filePath, "w+").close()

        with open(filePath, "w+") as f:
            f.write(str(os.getpid()))

    def driver(self):
        self.getProcessIDS()
        boards = self.fourchanconnectionhandler.getBoards()
        board_stack = []
        for board in boards:
            tmp_board = Board(board, self.fourchanconnectionhandler, self.databaseconnectionhandler)
            board_stack.append(tmp_board)
            print("initializing", board)

        while(len(board_stack) > 0):
            tmp_board = board_stack.pop()
            print("processing board", tmp_board)
            # call on board to process all topics
            tmp_board.processTopics()
            # put board object back in stack
            board_stack.append(tmp_board)