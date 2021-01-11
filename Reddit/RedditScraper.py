import datetime, threading, re, string, time, os

class RedditScraper():
    def __init__(self, datetimeobject, redditconnectionhandler, databaseconnectionhandler):
        self.datetimeobject = datetimeobject
        self.redditconnectionhandler = redditconnectionhandler
        self.databaseconnectionhandler = databaseconnectionhandler

    def addDayToTimestamp(self):
        return self.datetimeobject + datetime.timedelta(days=1)

    def getStandardDeviation(self, values):
        mean = sum(values)/len(values)
        subtract_mean_square_result = [(x-mean)**2 for x in values]
        mean_of_squared_differences = sum(subtract_mean_square_result)/len(subtract_mean_square_result)
        standard_deviation = mean_of_squared_differences**(1/2)
        return standard_deviation

    def getMean(self, values):
        return sum(values)/len(values)

    def getSubredditsToVisit(self, submission_metadata):
        score_array = [x["score"] for x in submission_metadata]
        #gild_1_array = [x["gildings"]["gid_1"] for x in submission_metadata]
        #gild_2_array = [x["gildings"]["gid_2"] for x in submission_metadata]
        #gild_3_array = [x["gildings"]["gid_3"] for x in submission_metadata]
        num_comments_array = [x["num_comments"] for x in submission_metadata]
        subreddit_subscribers_array = [x["subreddit_subscribers"] for x in submission_metadata]

        score_standard_deviation = self.getStandardDeviation(score_array)
        #gild_1_standard_deviation = self.getStandardDeviation(gild_1_array)
        #gild_2_standard_deviation = self.getStandardDeviation(gild_2_array)
        #gild_3_standard_deviation = self.getStandardDeviation(gild_3_array)
        num_comments_standard_deviation = self.getStandardDeviation(num_comments_array)
        subreddit_subscribers_standard_deviation = self.getStandardDeviation(subreddit_subscribers_array)

        score_mean = self.getMean(score_array)
        #gild_1_mean = self.getMean(gild_1_array)
        #gild_2_mean = self.getMean(gild_2_array)
        #gild_3_mean = self.getMean(gild_3_array)
        num_comments_mean = self.getMean(num_comments_array)
        subreddit_subscribers_mean = self.getMean(subreddit_subscribers_array)


        score_subreddits = [x["subreddit_id"] for x in submission_metadata if x["score"] >= score_mean+score_standard_deviation*2]
        #gild_1_subreddits = [x["subreddit_id"] for x in submission_metadata if x["gildings"]["gid_1"] >= gild_1_mean+gild_1_standard_deviation*2]
        #gild_2_subreddits = [x["subreddit_id"] for x in submission_metadata if x["gildings"]["gid_2"] >= gild_2_mean+gild_2_standard_deviation*2]
        #gild_3_subreddits = [x["subreddit_id"] for x in submission_metadata if x["gildings"]["gid_3"] >= gild_3_mean+gild_3_standard_deviation*999999999999999999999999999999999999]
        num_comments_subreddits = [x["subreddit_id"] for x in submission_metadata if x["num_comments"] >= num_comments_mean+num_comments_standard_deviation*2]
        subreddit_subscribers_subreddits = [x["subreddit_id"] for x in submission_metadata if x["subreddit_subscribers"] >= subreddit_subscribers_mean+subreddit_subscribers_standard_deviation*2]

        return set(score_subreddits + num_comments_subreddits + subreddit_subscribers_subreddits)
 
    def getCommentsFromSubmission(self, submission_id, begindate):
        data = self.redditconnectionhandler.getAllComments(submission_id, begindate)
        for entry in data:
            comment = entry["body"]
            date = entry["created_utc"]
            date = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
            final_dictionary = {date : comment.lower()}
            threading.Thread(target=self.databaseconnectionhandler.insertWordIntowordcount, args=("reddit", final_dictionary,)).start()            
            #self.databaseconnectionhandler.insertWordIntowordcount("reddit", final_dictionary)

    def getCommentsFromSubmissions(self, submission_metadata, subreddits_to_visit):
        submission_threads = []
        for submission in submission_metadata:
            if (submission["subreddit_id"] in subreddits_to_visit and int(submission["num_comments"]) > 0):
                submission_id = submission["id"]
                begindate = self.datetimeobject
                submission_thread = threading.Thread(target=self.getCommentsFromSubmission, args=(submission_id, begindate,))
                submission_threads.append(submission_thread)
                #break # DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE 

        print("len of submission threads", len(submission_threads))


        for i in range(0, len(submission_threads), 120):
            minute_timer = datetime.datetime.now() + datetime.timedelta(seconds=60)
            r = range(min(120, len(submission_threads) - i))
            for j in r:
                #print("starting thread", i+j)
                submission_threads[i+j].start()
            for j in r:
                #print("joining thread", i+j)
                submission_threads[i+j].join()
            while(datetime.datetime.now() < minute_timer):
                print("sleeping")
                time.sleep(1)


    def getProcessIDS(self):
        pwd = os.getcwd()
        filePath = os.path.join(pwd, "processIDS", "processIDS-reddit.txt")
        open(filePath, "w+").close()

        with open(filePath, "w+") as f:
            f.write(str(os.getpid()))

    def driver(self):
        self.getProcessIDS()
        print("before submission metadata")
        submission_metadata = self.redditconnectionhandler.getAllSubmissionsMetaData(self.datetimeobject)
        print("before subreddits to visit")
        subreddits_to_visit = self.getSubredditsToVisit(submission_metadata)
        print("before getcomments from submissions")
        self.getCommentsFromSubmissions(submission_metadata, subreddits_to_visit)
        print("before stopwatch")
        self.redditconnectionhandler.stopwatch.closeThread()
        print("after stopwatch")