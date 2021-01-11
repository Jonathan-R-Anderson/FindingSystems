import time, urllib, datetime, json, threading, random


class Timer(threading.Thread):
    def __init__(self):
        self.lock = threading.Lock()
        self.num_calls = 0
        self.max_calls = 120
        self.isDead = False
        super(Timer, self).__init__()

    def run(self):
        while(1):
            if (not self.isDead):
                print("resetting num_calls")
                self.num_calls = 0
            else:
                break
            time.sleep(60)

    def closeThread(self):
        self.isDead = True


'''
class MetaDataThread(threading.Thread):
    def __init__(self, url, stopwatch, logger):
        self.url = url
        self.data = []
        self.stopwatch = stopwatch
        self.logger = logger
        super(MetaDataThread, self).__init__()

    def run(self):
        network_sleep_time = 1
        stopwatch_sleep_time = 1
        while(1):
            try:
                if (self.stopwatch.num_calls < self.stopwatch.max_calls):
                    self.stopwatch.num_calls += 1
                    print("url", self.url)
                    with urllib.request.urlopen(self.url) as url:
                        data = json.loads(url.read().decode())
                        self.data = data["data"]
                        break
                else:
                    error = "Max calls reached"
                    self.logger.commit(0,"MetaDataThread","run",error)
                    time.sleep(stopwatch_sleep_time)
                    stopwatch_sleep_time += 2
            except urllib.error.HTTPError as e:
                if e.code in [429, 500, 502, 503, 504]:
                    error = "PushShift is down (error %s)" % (e.code)
                    self.logger.commit(1,"MetaDataThread","run",error)
                    time.sleep(network_sleep_time)
                    network_sleep_time *= 2
            except Exception as e:
                error = e
                self.logger.commit(2, "MetaDataThread","run",error)
'''


class MetaDataThread(threading.Thread):
    def __init__(self, url, stopwatch, logger, numFails=0):
        self.url = url
        self.data = []
        self.stopwatch = stopwatch
        self.logger = logger
        self.numFails = 0
        self.isDead = False
        self.isRunning = False
        self.failedAttempt = False
        super(MetaDataThread, self).__init__()

    def run(self):
        network_sleep_time = 1
        stopwatch_sleep_time = 1
        while(1):
            try:
                self.isRunning = True
                if (self.stopwatch.num_calls < self.stopwatch.max_calls):
                    self.stopwatch.num_calls += 1
                    req = urllib.request.Request(
                        self.url, 
                        data=None, 
                        headers={
                        'User-Agent': 'Python Bot Contact jranderson404@gmail.com'
                        }
                    )

                    with urllib.request.urlopen(req) as url:
                        data = json.loads(url.read().decode())
                        self.data = data["data"]
                        break
                else:
                    error = "Max calls reached"
                    self.logger.commit(0,"MetaDataThread","run",error)
                    time.sleep(stopwatch_sleep_time)
                    stopwatch_sleep_time += 2
            except urllib.error.HTTPError as e:
                if e.code in [429, 500, 502, 503, 504]:
                    error = "PushShift is down (error %s)" % (e.code)
                    self.logger.commit(1,"MetaDataThread","run",error)
                    time.sleep(network_sleep_time)
                    network_sleep_time *= 2
                    self.numFails = 0
                    self.failedAttempt = True
            except Exception as e:
                error = e
                self.logger.commit(2, "MetaDataThread","run",error)
                self.numFails = 100000
                self.failedAttempt = True
            self.isRunning = False
            self.isDead = True
        
                
'''
class CommentThread(threading.Thread):
    def __init__(self, url, stopwatch, enddateutc, submission_id, logger):
        self.url = url
        self.data = []
        self.stopwatch = stopwatch
        self.enddateutc = enddateutc
        self.submission_id = submission_id
        self.logger = logger
        self.isDead = False
        super(CommentThread, self).__init__()

    def run(self):
        network_sleep_time = 1
        stopwatch_sleep_time = 1
        while(1):
            try:
                if (self.stopwatch.num_calls < self.stopwatch.max_calls):
                    self.stopwatch.num_calls += 1
                    with urllib.request.urlopen(self.url) as url:
                        data = json.loads(url.read().decode())
                        self.data += data["data"]
                        len_data = len(data["data"])
                        if (len_data == 1000):
                            begindateutc = data["data"][len_data-1]["created_utc"]
                            self.url = "https://api.pushshift.io/reddit/comment/search/?link_id="+str(self.submission_id)+"&after="+str(begindateutc)+"&before="+str(self.enddateutc)+"&limit=1000&filter=body,created_utc"
                        else:
                            self.isDead = True
                            break
                else:
                    error = "Max calls reached"
                    self.logger.commit(0, "CommentThread", "run", error)
                    time.sleep(stopwatch_sleep_time)
                    stopwatch_sleep_time += 2 

            except urllib.error.HTTPError as e:
                if e.code in [429, 500, 502, 503, 504]:
                    error = "PushShift is down (error %s)" % (e.code)
                    self.logger.commit(1, "CommentThread", "run", error)
                    time.sleep(network_sleep_time)
                    network_sleep_time *= 2
            except Exception as e:
                error = e
                self.logger.commit(2, "CommentThread", "run", error)
'''

class CommentThread(threading.Thread):
    def __init__(self, url, stopwatch, enddateutc, submission_id, logger):
        self.url = url
        self.data = []
        self.stopwatch = stopwatch
        self.enddateutc = enddateutc
        self.submission_id = submission_id
        self.logger = logger
        self.isDead = False
        super(CommentThread, self).__init__()

    def run(self):
        network_sleep_time = 1
        stopwatch_sleep_time = 1
        handled_error_count = 0
        while(1):
            if (handled_error_count >= 5):
                break
            try:
                if (self.stopwatch.num_calls < self.stopwatch.max_calls):
                    self.stopwatch.num_calls += 1
                    #print("total calls made", self.stopwatch.num_calls)
                    req = urllib.request.Request(
                        self.url, 
                        data=None, 
                        headers={
                        'User-Agent': 'Python Bot Contact joe@user.com'
                        }
                    )
                    with urllib.request.urlopen(req) as url:
                        data = json.loads(url.read().decode())
                        self.data += data["data"]
                        len_data = len(data["data"])
                        if (len_data == 1000):
                            begindateutc = data["data"][len_data-1]["created_utc"]
                            self.url = "https://api.pushshift.io/reddit/comment/search/?link_id="+str(self.submission_id)+"&after="+str(begindateutc)+"&before="+str(self.enddateutc)+"&limit=1000&filter=body,created_utc"
                        else:
                            self.isDead = True
                            break
                else:
                    error = "Max calls reached"
                    self.logger.commit(0, "CommentThread", "run", error)
                    time.sleep(stopwatch_sleep_time)
                    stopwatch_sleep_time += 2 

            except urllib.error.HTTPError as e:
                if e.code in [429, 500, 502, 503, 504]:
                    error = "PushShift is down (error %s)" % (e.code)
                    self.logger.commit(1, "CommentThread", "run", error)
                    time.sleep(network_sleep_time)
                    network_sleep_time *= 2
                    handled_error_count += 1
            except Exception as e:
                error = e
                self.logger.commit(2, "CommentThread", "run", error)
                break
                    
class RedditConnectionHandler:
    def __init__(self, logger):
        self.logger = logger
        self.stopwatch = Timer()
        self.stopwatch.start()

    def addMinuteToTimestamp(self, timestamp):
        return timestamp + datetime.timedelta(minutes=30) #THIS IS NOW ADDING 30 MINUTES INSTEAD OF 1

    def addDayToTimestamp(self, timestamp):
        return timestamp + datetime.timedelta(days=1)

    def generateMetaDataURLS(self, begindate):
        urls = []
        begindateutc = int(begindate.timestamp())
        enddate = self.addMinuteToTimestamp(begindate)
        enddateutc = int(enddate.timestamp())
        nextdayutc = int(self.addDayToTimestamp(begindate).timestamp())
        going_by_minute = False
        while True:
            url_string = "https://api.pushshift.io/reddit/submission/search/?after="+str(begindateutc)+"&before="+str(enddateutc)+"&limit=1000&filter=id,score,gildings,num_comments,subreddit_subscribers,subreddit_id"
            urls.append(url_string)
            begindate = self.addMinuteToTimestamp(begindate)
            begindateutc = int(begindate.timestamp())
            enddate = self.addMinuteToTimestamp(enddate)
            enddateutc = int(enddate.timestamp())
            if (enddateutc >= nextdayutc):
                break
        return urls

    def generateCommentURLS(self, submission_id, begindate):
        begindateutc = int(begindate.timestamp())
        url = ["https://api.pushshift.io/reddit/comment/search/?link_id="+str(submission_id)+"&after="+str(begindateutc)+"&limit=1000&filter=body,created_utc"]
        return url

    def getAllSubmissionsMetaData(self, begindate):
        urls = self.generateMetaDataURLS(begindate)
        metadata_threads = []
        metadata = []
        for i in range(0, len(urls), 120):
            minute_timer = datetime.datetime.now() + datetime.timedelta(seconds=60)
            r = range(min(120, len(urls) - i))
            for j in r:
                metadata_thread = MetaDataThread(urls[i+j], self.stopwatch, self.logger)
                metadata_threads.append(metadata_thread)
                metadata_thread.start()
            for j in r:
                metadata_threads[i+j].join()
                for dictionary in metadata_threads[i+j].data:
                    metadata.append(dictionary)
            while(datetime.datetime.now() < minute_timer):
                print("sleeping")
                time.sleep(1)

        return metadata


    def getAllComments(self, submission_id, begindate):
        urls = self.generateCommentURLS(submission_id, begindate) # generates a single URL
        metadata_threads = []
        metadata = []
        for url in urls:
            metadata_thread = CommentThread(url, self.stopwatch, int(self.addDayToTimestamp(begindate).timestamp()), submission_id, self.logger)
            metadata_threads.append(metadata_thread)

        for thread in metadata_threads:
            thread.start()
        for thread in metadata_threads:
            thread.join()

        for thread in metadata_threads:
            for dictionary in thread.data:
                metadata.append(dictionary)
        return metadata