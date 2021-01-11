import threading, time, random, datetime, re, sys, gc


class TopicScraper(threading.Thread):
    def __init__(self, board, topic, databaseconnectionhandler):
        self.board = board
        self.topic = topic
        self.databaseconnectionhandler = databaseconnectionhandler
        super(TopicScraper, self).__init__()

    def removeTimeOfDayFromTimestamp(self, timestamp): # no longer used
        date_time_array =  str(timestamp).split(" ")
        date_array = [int(x) for x in date_time_array[0].split("-")]
        time_array = [int(float(x)) for x in date_time_array[1].split(":")]
        datetimestamp = datetime.datetime(date_array[0], date_array[1], date_array[2], time_array[0], time_array[1], time_array[2]).replace(hour=0,minute=0,second=0)
        return datetimestamp

    def run(self):
        wait_time = 0 # variable set to wait before refreshing the page to check for new posts - so that the cpu doesn't burn up cycles
        final_dictionary = {} # {Date: [ sentences are here, this is a second sentence, okay ]}
        replies = [] # array of reply.post_id - same type of mechanism used in live_topics, so we only get new replies
        while(not self.topic.sticky and not self.topic.is_404 and not self.topic.closed and not self.topic.archived): # while the topic is none of these conditions, iterate
            if (self.topic.update() > 0): # checks to see if there are new posts, if the number of new posts are greater than 0, reset the timer back to 5 seconds
                wait_time = 5
            else:
                wait_time += 5
            new_replies =  [reply for reply in self.topic.all_posts if reply.post_id not in replies] # get only the new replies
            for reply in new_replies:
                replies.append(reply.post_id)
                #reply_date = int(self.removeTimeOfDayFromTimestamp(reply.datetime).timestamp())
                reply_date = int(reply.datetime.timestamp())
                if (reply_date not in final_dictionary.keys()):
                    final_dictionary[reply_date] = [reply.comment.lower()] # create new entry for a comment at the specified date in the dictionary
                else:
                    final_dictionary[reply_date].append(reply.comment.lower()) # if entry for a comment's date already exists, append the comment to an array
            time.sleep(wait_time)

        for date in final_dictionary.keys():
            database_date = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S') # formatting the date for the database
            for comment in final_dictionary[date]: # iterate through all comments for a specific datetime
                def striphtml(data):
                    p = re.compile(r'<.*?>|&gt|gt') # regular expression to strip out special characters at the beginning of the comment
                    return p.sub('', data)
                comment = striphtml(comment)
                self.databaseconnectionhandler.insertWordIntowordcount("4chan", {database_date : comment}) # commit the data to the database
        gc.collect()
        print("thread collected", gc.get_stats())


class BoardScraper(threading.Thread):
    def __init__(self, fourchanconnectionhandler, board, databaseconnectionhandler):
        self.fourchanconnectionhandler = fourchanconnectionhandler
        self.board = board
        self.databaseconnectionhandler = databaseconnectionhandler
        super(BoardScraper, self).__init__()

    def run(self): # in place of a driver method
        live_topics = [] # array of current topic id's for running threads
        live_topic_threads = [] # array of threads for each new topic being monitored
        while(1):
            new_topics = [topic for topic in self.fourchanconnectionhandler.getTopics(self.board) if topic.id not in live_topics] # generates array of topics to scrape based on whether or not their id is in live_topics
            for topic in new_topics:
                if (not topic.sticky and not topic.is_404 and not topic.closed and not topic.archived): # condition where we only get user generated topics that are currently active on 4chan
                    live_topics.append(topic.id)
                    topic_thread = TopicScraper(self.board, topic, self.databaseconnectionhandler) # topic scraper thread
                    topic_thread.start()
                    live_topic_threads.append(topic_thread)
            next_live_topic_threads = []
            deleted_threads = []
            for thread in live_topic_threads: # for every iteration of the loop, check every thread to see if the topic is no longer active
                if (not thread.isAlive()): # if the topic is no longer active then...
                    thread.join()
                    live_topics.remove(thread.topic.id)
                    #live_topic_threads.remove(thread)
                    deleted_threads.append(thread)
                    del thread
                else:
                    next_live_topic_threads.append(thread) # creating new array of only the active topic threads
            for thread in deleted_threads:
                live_topic_threads.remove(thread)
            del deleted_threads
            del live_topic_threads
            live_topic_threads = next_live_topic_threads # setting the new active topic threads equal to the old list of active topic threads
            del next_live_topic_threads
            print("len of live topics", len(live_topics), "for board", self.board)
            print("len of live topic threads", len(live_topic_threads), "for board", self.board)
            gc.collect()
            print("collected", gc.get_stats())
            time.sleep(random.randint(15, 60)) # sleep as to not burn up cpu cycles

