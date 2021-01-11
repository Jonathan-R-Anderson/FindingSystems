import datetime, urllib, random
from newsapi import NewsApiClient
from bs4 import BeautifulSoup

class NewsConnectionHandler:
    def __init__(self, api_key, logger):
        self.api_key = api_key
        self.logger = logger
        self.client = NewsApiClient(api_key=self.api_key)

    def addDayToTimestamp(self, timestamp):
        return timestamp + datetime.timedelta(days=1)

    def convertTimestampToString(self, timestamp):
        date_time_array =  str(timestamp).split(" ")
        return date_time_array[0]

    def getSources(self):
        while(1):
            sources = self.client.get_sources()
            if (sources["status"] == "ok"):
                source_ids = [source["id"] for source in sources["sources"]]
                return source_ids
            else:
                return "error"

    def getEverything(self,sources,from_param):
        to = self.convertTimestampToString(self.addDayToTimestamp(from_param))
        from_param = self.convertTimestampToString(from_param)
        while(1):
            sources = ",".join(sources)
            articles = self.client.get_everything(sources=sources,from_param=from_param,to=to,page_size=100,page=1)
            if (articles["status"] == "ok"):
                num_results = articles["totalResults"]
                num_pages = int(num_results/100)+1
                ''' Need to pay for subscription in order to get anymore results
                for i in range(1,num_pages):
                    articles = self.client.get_everything(sources=sources,from_param=from_param,to=to,page_size=100,page=i)
                    urls = [x["url"] for x in articles["articles"]]
                    print(urls)
                '''
                urls = [x["url"] for x in articles["articles"]]

                return urls

    def getUserAgent(self):
        platform = random.choice(['Macintosh', 'Windows', 'X11'])
        if platform == 'Macintosh':
            os  = random.choice(['68K', 'PPC'])
        elif platform == 'Windows':
            os  = random.choice(['Win3.11', 'WinNT3.51', 'WinNT4.0', 'Windows NT 5.0', 'Windows NT 5.1', 'Windows NT 5.2', 'Windows NT 6.0', 'Windows NT 6.1', 'Windows NT 6.2', 'Win95', 'Win98', 'Win 9x 4.90', 'WindowsCE'])
        elif platform == 'X11':
            os  = random.choice(['Linux i686', 'Linux x86_64'])
        browser = random.choice(['chrome', 'firefox', 'ie'])
        if browser == 'chrome':
            webkit = str(random.randint(500, 599))
            version = str(random.randint(0, 24)) + '.0' + str(random.randint(0, 1500)) + '.' + str(random.randint(0, 999))
            return 'Mozilla/5.0 (' + os + ') AppleWebKit/' + webkit + '.0 (KHTML, live Gecko) Chrome/' + version + ' Safari/' + webkit
        elif browser == 'firefox':
            year = str(random.randint(2000, 2012))
            month = random.randint(1, 12)
            if month < 10:
                month = '0' + str(month)
            else:
                month = str(month)
            day = random.randint(1, 30)
            if day < 10:
                day = '0' + str(day)
            else:
                day = str(day)
            gecko = year + month + day
            version = random.choice(['1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0', '10.0', '11.0', '12.0', '13.0', '14.0', '15.0'])
            return 'Mozilla/5.0 (' + os + '; rv:' + version + ') Gecko/' + gecko + ' Firefox/' + version
        elif browser == 'ie':
            version = str(random.randint(1, 10)) + '.0'
            engine = str(random.randint(1, 5)) + '.0'
            option = random.choice([True, False])
            if option == True:
                token = random.choice(['.NET CLR', 'SV1', 'Tablet PC', 'Win64; IA64', 'Win64; x64', 'WOW64']) + '; '
            elif option == False:
                token = ''
            return 'Mozilla/5.0 (compatible; MSIE ' + version + '; ' + os + '; ' + token + 'Trident/' + engine + ')'
 

    def getTextFromURL(self, url):
        try:
            request = urllib.request.Request(url,
                                             data=None,
                                             headers={
                                                 "User-Agent":self.getUserAgent()})
            with urllib.request.urlopen(request, timeout=5) as url:
                html = url.read().decode("utf-8", "ignore")
                soup = BeautifulSoup(html,features="html.parser")

                for script in soup(["script", "style"]):
                    script.extract()

                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)
                return text
        except urllib.error.HTTPError as e:
            self.logger.commit(1, "NewsConnectionHandler", "getTextFromURL", e.code)
        except Exception as e:
                self.logger.commit(2, "NewsConnectionHandler", "getTextFromURL", e)
        return ""