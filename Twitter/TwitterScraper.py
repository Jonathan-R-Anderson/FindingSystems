import threading

class TrendThread(threading.Thread):
    def __init__(self, timestamp, trend, woeid, twitterconnectionhandler):
        self.timestamp = timestamp
        self.trend = trend
        self.woeid = woeid
        self.isDead = False
        self.twitterconnectionhandler = twitterconnectionhandler
        super(TrendThread, self).__init__()

    def run(self):
        since_id = -1
        previous_datetime = None
        while(1):
            since_id = self.twitterconnectionhandler.getStartingID(self.trend["name"])
            print("tweet array", tweet_array)

            self.isDead = True
            #break # DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE 

class WOEIDThread(threading.Thread):
    def __init__(self, timestamp, woeid, twitterconnectionhandler):
        self.timestamp = timestamp
        self.woeid = woeid
        self.twitterconnectionhandler = twitterconnectionhandler
        super(WOEIDThread, self).__init__()

    def run(self):
        trend_threads = []
        trend_names = []
        while(1):
            trends = None
            #trends = self.twitterconnectionhandler.getTrends(self.woeid)
            if (trends is not None):
                tmp_trends = [trend for trend in trends[0]["trends"] if trend["name"] not in trend_names]
                trend_names += [trend["name"] for trend in tmp_trends]
                for trend in tmp_trends:
                    break # DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE 
                    tmp_thread = TrendThread(self.timestamp, trend, self.woeid, self.twitterconnectionhandler)
                    trend_threads.append(tmp_thread)
                    tmp_thread.start()
            for thread in trend_threads:
                if (thread.isDead):
                    trend_names.remove(thread.trend["name"])
                    thread.join()
            break # DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE 

class TwitterScraper:
    def __init__(self, timestamp, twitterconnectionhandler):
        self.timestamp = timestamp
        self.twitterconnectionhandler = twitterconnectionhandler


    def driver(self):

        print("number of active accounts", self.twitterconnectionhandler.checkHowManyAccountsLoggedIn())




        thread_array = []
        woeid_array = self.twitterconnectionhandler.generateCountryWOEIDArray()
        for woeid in woeid_array:
            tmp_thread = WOEIDThread(self.timestamp, woeid, self.twitterconnectionhandler)
            thread_array.append(tmp_thread)
            tmp_thread.start()
            break # DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE 

        for thread in thread_array:
            thread_array.remove(thread)
            thread.join()