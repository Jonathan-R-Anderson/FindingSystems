import datetime, schedule, time, sys, os, threading

from multiprocessing import Process


dir_path = os.path.dirname(os.path.realpath(__file__))
pwd = os.path.join(dir_path)

sys.path.append(os.path.join(pwd,"Google_Trends"))
sys.path.append(os.path.join(pwd,"Database"))
sys.path.append(os.path.join(pwd,"EODData"))
sys.path.append(os.path.join(pwd,"AlphaVantage"))
sys.path.append(os.path.join(pwd,"FourChanStack"))
sys.path.append(os.path.join(pwd,"Reddit"))
sys.path.append(os.path.join(pwd,"Tagging"))
sys.path.append(os.path.join(pwd,"News"))
sys.path.append(os.path.join(pwd,"Logger"))
sys.path.append(os.path.join(pwd,"ML_Tagging"))
sys.path.append(os.path.join(pwd,"DiscordServers"))
sys.path.append(os.path.join(pwd,"BagOfWords"))
sys.path.append(os.path.join(pwd,"Google_Suggested_Queries"))
sys.path.append(os.path.join(pwd,"Proxy_Scraper"))
sys.path.append(os.path.join(pwd,"Bucket"))


from GoogleTrendsConnectionHandler import GoogleTrendsConnectionHandler
from GoogleTrendsScraper3 import GoogleTrendsScraper
from DatabaseConnectionHandler import DatabaseConnectionHandler
from EODDataConnectionHandler import EODDataConnectionHandler
from AlphaVantageScraper import AlphaVantageScraper
from AlphaVantageConnectionHandler import AlphaVantageConnectionHandler
from FourChanScraper import FourChanScraper
from FourChanConnectionHandler import FourChanConnectionHandler
from RedditConnectionHandler import RedditConnectionHandler
from RedditScraper import RedditScraper
from Tagger import Tagger
from NewsConnectionHandler import NewsConnectionHandler
from NewsScraper import NewsScraper
from Logger import Logger
from DiscordServersConnectionHandler import DiscordServersConnectionHandler
from ML_Tagger import ML_Tagger
from ML_Scraper import ML_Scraper
from BOWConnectionHandler import BOWConnectionHandler
from BOWScraper import BOWScraper
from GoogleSuggestedQueriesConnectionHandler import GoogleSuggestedQueriesConnectionHandler
from GoogleSuggestedQueriesScraper import GoogleSuggestedQueriesScraper
from ProxyScraper import ProxyScraper
from BucketConnectionHandler import BucketConnectionHandler
from BucketScraper import BucketScraper
from BucketPreprocessing import BucketPreprocessing

def removeTimeOfDayFromTimestamp(timestamp):
        date_time_array =  str(timestamp).split(" ")
        date_array = [int(x) for x in date_time_array[0].split("-")]
        time_array = [int(float(x)) for x in date_time_array[1].split(":")]
        datetimestamp = datetime.datetime(date_array[0], date_array[1], date_array[2], time_array[0], time_array[1], time_array[2]).replace(hour=0,minute=0,second=0)
        return datetimestamp

def reddit(logger, timestamp, dbch):
    timestamp = datetime.datetime.now() - datetime.timedelta(days=1)

    rch = RedditConnectionHandler(logger)
    rs = RedditScraper(timestamp, rch, dbch)
    rs.driver()

def news(logger, timestamp, dbch):
    api_key = ""
    nch = NewsConnectionHandler(api_key, logger)
    ns = NewsScraper(timestamp,nch, dbch)
    ns.driver()

def alphavantage(logger, timestamp, dbch):
    timestamp = datetime.datetime.now() - datetime.timedelta(days=1)
    eoddch = EODDataConnectionHandler()
    avch_apikey = ""
    avch_trial_apikey = ""
    avch = AlphaVantageConnectionHandler(avch_trial_apikey, logger)
    avs = AlphaVantageScraper(timestamp, avch, eoddch, dbch)
    avs.driver()

def google(logger, dbch):
    fuck = GoogleTrendsScraper(dbch, logger)
    fuck.driver()

def fourchan(dbch):
    fcch = FourChanConnectionHandler()
    fcs = FourChanScraper(fcch, dbch)
    fcs.driver()

def executeMultipleTimes(logger, timestamp, dbch):
    print("starting multiple times")

    pr = Process(target=reddit, args=(logger, timestamp, dbch,))
    pr.start()

    pn = Process(target=news, args=(logger, timestamp, dbch,))
    pn.start()

    pav = Process(target=alphavantage, args=(logger, timestamp, dbch))
    pav.start()


def executeOnce(logger, dbch):
    print("starting once")

    pg = Process(target=google, args=(logger, dbch,))
    pg.start()

    pfc = Process(target=fourchan, args=(dbch,))
    pfc.start()

if __name__ == '__main__':
    
    timestamp = datetime.datetime.now()

    host = ""
    host = ""
    user = ""
    passwd = ""
    db = ""
    dbch = DatabaseConnectionHandler(host, user, passwd, db)

    logger = Logger(dbch)


    #executeOnce(logger, dbch)

    #schedule.every().day.at("21:15").do(executeMultipleTimes, logger, timestamp, dbch)

    #while True:
    #    schedule.run_pending()
    #    time.sleep(60)


    # this has to be ran with entries in the company table, so make sure to run alphavantage scraper BEFORE running this
    #eoddch = EODDataConnectionHandler()
    #bowch = BOWConnectionHandler()
    #bows = BOWScraper(bowch, eoddch, dbch)
    #mls = ML_Scraper(bowch, bows, dbch, eoddch)
    #mltg = ML_Tagger(dbch, mls)
    #mltg.driver()



    ps = ProxyScraper()
    proxies = [] 
    proxy_dict = {}
    gsqch_array = []
    paid_proxies = [] # [("IP", PORT)]
    [proxies.append(x) for x in paid_proxies]
    [proxies.append(x) for x in ps.driver()]
    proxies = list(set(proxies))

    thread_lock = threading.Lock()
    num_proxies = len(proxies)
    for proxy in proxies:
        proxy_dict[proxy] = [False, False, False]
        tmp_gsqch = GoogleSuggestedQueriesConnectionHandler(proxy, proxy_dict, thread_lock)
        gsqch_array.append(tmp_gsqch)

    bch = BucketConnectionHandler()
    bs = BucketScraper(bch)
    buckets = bs.driver() # array of dicts [{industry-exchange : [(symbol_1, subsector_1), (symbol_2, subsector_2)]}]
    bpp = BucketPreprocessing(buckets, gsqch_array)
    buckets_scores = bpp.driver() # array of dicts [{industry-exchange : [(symbol_1, subsector_1, [scores, for,every,index]), (symbol_2, subsector_2,  [scores, for,every,index])]}, {"subsector"-subsector_name : [query_centroid, query_mean, query_stddev]}]
    gsqs = GoogleSuggestedQueriesScraper(gsqch_array, dbch, buckets_scores)
    gsqs.driver()