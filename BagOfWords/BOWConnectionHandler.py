from googlesearch import search
import urllib, random, ssl, time
from bs4 import BeautifulSoup

class BOWConnectionHandler:
    def __init__(self):
        pass

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

    def getURLSForCompany(self, num, company, start, stop):
        wait_time = 1
        while(1):
            try:
                urls = []
                url_results = search(company, tld="com", num=num, start=start, stop=stop, pause=2.0)
                for url in url_results:
                    urls.append(url)
                return urls

            except urllib.error.HTTPError as e:
                if (e.code in [429]):
                    print("Error", e.code, "sleeping for", wait_time)
                    time.sleep(wait_time)
                    wait_time *= 2

            except Exception as e:
                print("BOWConnectionHandler-getURLSForCompany Exception", e)

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
            #print("ERROR", e)
            #self.logger.commit(1, "NewsConnectionHandler", "getTextFromURL", e.code)
            pass
        except Exception as e:
            #print("ERROR", e)
            #self.logger.commit(2, "NewsConnectionHandler", "getTextFromURL", e)
            pass
        return ""