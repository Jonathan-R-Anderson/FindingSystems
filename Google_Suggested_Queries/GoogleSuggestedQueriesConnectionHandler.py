import urllib, random, re, time, requests

class GoogleSuggestedQueriesConnectionHandler:
    def __init__(self, proxy, proxies, thread_lock):
        self.proxy = proxy
        self.proxies = proxies
        self.thread_lock = thread_lock
        self.base_url = "https://suggestqueries.google.com/complete/search?"
        self.jquery_val_p1 = 17208370971317210432
        self.jquery_val_p2 = 1000000000000
        #self.setProxyInUse()

    def setProxyNotInUse(self):
        with self.thread_lock:
            self.proxies[self.proxy][0] = False

    def setProxyInUse(self):
        with self.thread_lock:
            self.proxies[self.proxy][0] = True # set proxy as being in use

    def setBadProxy(self):
        with self.thread_lock:
            self.proxies[self.proxy][0] = False # not in use
            self.proxies[self.proxy][1] = True # bad proxy

    def setPenalizedProxy(self):
        with self.thread_lock:
            self.proxies[self.proxy][0] = False # not in use
            self.proxies[self.proxy][2] = True # penalized

    def updatePenalizedProxy(self, proxy):
         with self.thread_lock:
            self.proxies[self.proxy][2] = False # not penalized  

    def switchProxy(self):
        former_proxy = self.proxy
        #print("waiting for lock")
        with self.thread_lock:
            self.proxies[self.proxy][0] = False # old proxy no longer in use
            #print("proxy", self.proxy, "proxy value", self.proxies[self.proxy])
            #print("Switching proxies")
            proxy = list(self.proxies.keys())[random.randint(0,len(list(self.proxies.keys()))-1)]
            #print("proxy_key", proxy_key)
            #proxy = self.proxies[proxy_key]
            if (proxy is not former_proxy):
                proxy_values = self.proxies[proxy]
                in_use = proxy_values[0]
                bad_proxy = proxy_values[1]
                penalized = proxy_values[2]
                #print("testing proxy", proxy, self.proxies[proxy])
                if ((not in_use and not bad_proxy and penalized)):
                    if (not self.testProxy(proxy)):
                        self.proxies[self.proxy][2] = False # not penalized  
                        #print("proxy", proxy, "is no longer penalized")
                if ((not in_use and not bad_proxy)
                    or (not in_use and not penalized)):
                    #print("choosing proxy", proxy)
                    self.proxy = proxy
                    #print("before setting proxy in use inside switchProxy")
                    self.proxies[self.proxy][0] = True # set proxy as being in use
                    #print("before returning inside of switchProxy")
                    return
            self.proxies[self.proxy][0] = True # old proxy back in use



    def testProxy(self, proxy):
        url = "https://suggestqueries.google.com/complete/search?jsonp=jQuery17208370971317210432_1000000000000&q=Testing+this+thing&client=chrome&_=1565244003246"
        bad_proxy = False
        try:
            proxy = {
                    "https" : "https://"+proxy[0]+":"+proxy[1]
                    }

            headers = {
                      "User-Agent" : self.getUserAgent(),
                      "Connection" : "close"
                      }

            response = requests.get(url, headers=headers, proxies=proxy)
            if (response.status_code is 200):
                data = response.text
            else:
                bad_proxy = True
        except Exception as e:
            bad_proxy = True


        return bad_proxy

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
                             
    def generateURL(self, query):
        return self.base_url + "jsonp=jQuery%s_%s&q=%s&client=chrome&_=1565244003246"  % (self.jquery_val_p1,self.jquery_val_p2,query)

    def getTextFromURL(self, url):
        self.setProxyInUse()
        #sleep_time = 1
        #number_of_attempts = 0
        while(1):
            try:
                proxy = {
                        "https" : "https://"+self.proxy[0]+":"+self.proxy[1]
                        }

                headers = {
                          "User-Agent" : self.getUserAgent(),
                          "Connection" : "close"
                          }

                response = requests.get(url, headers=headers, proxies=proxy)
                if (response.status_code in [403]):
                    self.setPenalizedProxy()
                    #print("before switchproxy")
                    self.switchProxy()
                    #print("403 ERROR, switching proxy to", self.proxy)
                    #print("after switchproxy")
                    #sleep_time *= 2
                elif (response.status_code is 200):
                    suggested_queries = response.text
                    suggested_queries = re.search(r'\(\["(.*?)\],\[', suggested_queries).group(1)
                    suggested_queries = suggested_queries.split(",")
                    suggested_queries_dirty = suggested_queries[1:len(suggested_queries)-1]
                    suggested_queries_clean = [query.replace('"', "").replace("[", "") for query in suggested_queries_dirty]
                    #print("suggested_queries_clean", suggested_queries_clean)
                    self.setProxyNotInUse()
                    return suggested_queries_clean
                else:
                    print("ERROR in response code", response.status_code)
            except Exception as e:
                #print("ERROR bad proxy, switching proxy to", self.proxy)
                #self.setBadProxy()
                self.switchProxy()              
                #if ("Max retries exceeded with url" in str(e)):
                #    #print("Error 1", e)
                #    #self.setPenalizedProxy()
                #    self.setBadProxy() # i don't know which one to use
                #    self.switchProxy()
                #elif ("EOF occurred in violation of protocol" in str(e)):
                #    #print("Error 2", str(e))
                #    self.setBadProxy()
                #    self.switchProxy()
                #else:
                #    #print("Error 3", str(e))
                #    self.setBadProxy()
                #    self.switchProxy()
                #    #sleep_time = 1
            #print("sleeping for", sleep_time)
            #time.sleep(sleep_time)
