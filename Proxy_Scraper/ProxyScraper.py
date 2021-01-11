import urllib, re, random
from time import gmtime, strftime, sleep

class ProxyScraper:
    def isnum(self, ch):
        if ch == "0":
            return True
        if ch == "1":
            return True
        if ch == "2":
            return True
        if ch == "3":
            return True
        if ch == "4":
            return True
        if ch == "5":
            return True
        if ch == "6":
            return True
        if ch == "7":
            return True
        if ch == "8":
            return True
        if ch == "9":
            return True
        return False
    
    def alfabetcheck(self, line):
        sw = False
        if "a" in line:
            sw = True
        if "b" in line:
            sw = True
        if "c" in line:
            sw = True
        if "d" in line:
            sw = True
        if "e" in line:
            sw = True
        if "f" in line:
            sw = True
        if "g" in line:
            sw = True
        if "h" in line:
            sw = True
        if "i" in line:
            sw = True
        if "j" in line:
            sw = True
        if "k" in line:
            sw = True
        if "l" in line:
            sw = True
        if "m" in line:
            sw = True
        if "n" in line:
            sw = True
        if "o" in line:
            sw = True
        if "p" in line:
            sw = True
        if "q" in line:
            sw = True
        if "r" in line:
            sw = True
        if "s" in line:
            sw = True
        if "t" in line:
            sw = True
        if "u" in line:
            sw = True
        if "v" in line:
            sw = True
        if "w" in line:
            sw = True
        if "x" in line:
            sw = True
        if "y" in line:
            sw = True
        if "z" in line:
            sw = True
        if sw == True:
            return False
        else:
            return True


    def process(self, source):
        proxies = []
    
        result = re.findall('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?=[^\d])\s*:?\s*(\d{2,5})', source)
        [proxies.append(x) for x in result]
        return proxies
    

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

        
    def driver(self):  
        urls = ["http://aliveproxy.com/anonymous-proxy-list",
        "http://aliveproxy.com/ca-proxy-list",
        "http://aliveproxy.com/fastest-proxies",
        "http://aliveproxy.com/fr-proxy-list",
        "http://aliveproxy.com/gb-proxy-list",
        "http://aliveproxy.com/high-anonymity-proxy-list",
        "http://aliveproxy.com/jp-proxy-list",
        "http://aliveproxy.com/proxy-list-port-3128",
        "http://aliveproxy.com/proxy-list-port-80",
        "http://aliveproxy.com/proxy-list-port-8000",
        "http://aliveproxy.com/proxy-list-port-8080",
        "http://aliveproxy.com/ru-proxy-list",
        "http://aliveproxy.com/us-proxy-list",
        "http://atomintersoft.com/anonymous_proxy_list",
        "http://atomintersoft.com/high_anonymity_elite_proxy_list",
        "http://atomintersoft.com/products/alive-proxy/proxy-list",
        "http://atomintersoft.com/products/alive-proxy/proxy-list?ap=9",
        "http://atomintersoft.com/products/alive-proxy/proxy-list/3128",
        "http://atomintersoft.com/products/alive-proxy/proxy-list/com",
        "http://atomintersoft.com/products/alive-proxy/proxy-list/high-anonymity/",
        "http://atomintersoft.com/products/alive-proxy/socks5-list",
        "http://atomintersoft.com/proxy_list_domain_com",
        "http://atomintersoft.com/proxy_list_domain_edu",
        "http://atomintersoft.com/proxy_list_domain_net",
        "http://atomintersoft.com/proxy_list_domain_org",
        "http://atomintersoft.com/proxy_list_port_3128",
        "http://atomintersoft.com/proxy_list_port_80",
        "http://atomintersoft.com/proxy_list_port_8000",
        "http://atomintersoft.com/proxy_list_port_81",
        "http://atomintersoft.com/transparent_proxy_list",
        "http://best-proxy.com/english/search.php?search=anonymous-and-elite&country=any&type=anonymous-and-elite&port=any&ssl=any",
        "http://best-proxy.com/english/search.php?search=anonymous-and-elite&country=any&type=anonymous-and-elite&port=any&ssl=any&p=2",
        "http://best-proxy.com/english/search.php?search=anonymous-and-elite&country=any&type=anonymous-and-elite&port=any&ssl=any&p=3",
        "http://bestproxy.narod.ru/proxy2.html",
        "http://checkerproxy.net/all_proxy",
        "http://ejohn.org/apps/anon/",
        "http://free-proxy-list.net/",
        "http://free-proxy-list.net/anonymous-proxy.html",
        "http://free-proxy-list.net/uk-proxy.html",
        "http://multiproxy.org/anon_proxy.htm",
        "http://multiproxy.org/txt_all/proxy.txt",
        "http://nntime.com/proxy-list-01.htm",
        "http://nntime.com/proxy-list-02.htm",
        "http://nntime.com/proxy-list-03.htm",
        "http://nntime.com/proxy-list-04.htm",
        "http://nntime.com/proxy-list-05.htm",
        "http://nntime.com/proxy-list-06.htm",
        "http://nntime.com/proxy-list-07.htm",
        "http://nntime.com/proxy-list-08.htm",
        "http://nntime.com/proxy-list-09.htm",
        "http://nntime.com/proxy-list-10.htm",
        "http://nntime.com/proxy-list-11.htm",
        "http://nntime.com/proxy-list-12.htm",
        "http://nntime.com/proxy-list-13.htm",
        "http://nntime.com/proxy-list-14.htm",
        "http://nntime.com/proxy-list-15.htm",
        "http://nntime.com/proxy-list-17.htm",
        "http://nntime.com/proxy-list-18.htm",
        "http://nntime.com/proxy-list-19.htm",
        "http://nntime.com/proxy-list-20.htm",
        "http://nntime.com/proxy-list-21.htm",
        "http://nntime.com/proxy-list-22.htm",
        "http://nntime.com/proxy-list-23.htm",
        "http://nntime.com/proxy-list-24.htm",
        "http://nntime.com/proxy-list-25.htm",
        "http://nntime.com/proxy-list-27.htm",
        "http://nntime.com/proxy-list-28.htm",
        "http://nntime.com/proxy-list-29.htm",
        "http://nntime.com/proxy-list-30.htm",
        "http://rootjazz.com/proxies/proxies.txt",
        "http://spys.ru/en/anonymous-proxy-list/",
        "http://spys.ru/en/free-proxy-list/",
        "http://tools.rosinstrument.com/proxy/?rule1",
        "http://www.getproxy.jp/en/default/1",
        "http://www.getproxy.jp/en/default/2",
        "http://www.getproxy.jp/en/default/3",
        "http://www.getproxy.jp/en/default/4",
        "http://www.getproxy.jp/en/default/5",
        "http://www.google-proxy.net/",
        "http://www.ip-adress.com/proxy_list/?k=time&d=desc",
        "http://www.my-proxy.com/free-proxy-list.html",
        "http://www.proxy4ever.com/",
        "http://www.proxyblind.org/anonymous-proxy.shtml",
        "http://www.proxyblind.org/free-proxy.shtml",
        "http://www.proxyblind.org/proxy-list.shtml",
        "http://www.proxyblind.org/ssl.shtml",
        "http://www.proxyforest.com/proxy.htm",
        "http://www.socks-proxy.net/",
        "http://www.ultrasurf.org/",
        "http://www.us-proxy.org/",
        "http://spys.one/en/",
        "http://spys.one/en/http-proxy-list/",
        "http://spys.one/en/anonymous-proxy-list/",
        "http://spys.one/en/non-anonymous-proxy-list/",
        "http://spys.one/en/socks-proxy-list/",
        "https://free-proxy-list.net/",
        "http://www.gatherproxy.com/",
        "https://www.proxynova.com/proxy-server-list/",
        "https://www.proxy-list.download/api/v0/get?l=en&t=http",
        "https://www.proxy-list.download/api/v0/get?l=en&t=https",
        "https://www.proxy-list.download/api/v0/get?l=en&t=socks4",
        "https://www.proxy-list.download/api/v0/get?l=en&t=socks5",
        "https://sockslist.net/proxy/server-socks-hide-ip-address/",
        "https://sockslist.net/proxy/server-socks-hide-ip-address/2",
        "https://sockslist.net/proxy/server-socks-hide-ip-address/3",
        "https://sockslist.net/proxy/server-socks-hide-ip-address/4",
        "https://www.proxyrack.com/free-proxy-list/",
        "https://www.my-proxy.com/free-socks-5-proxy.html",
        "https://list.proxylistplus.com/Socks-List-1",
        "https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-2",
        "http://proxydb.net/?protocol=http&protocol=https&protocol=socks4&protocol=socks5&country=",
        "http://proxysearcher.sourceforge.net/Proxy%20List.php?type=http&filtered=true",
        "http://proxysearcher.sourceforge.net/Proxy%20List.php?type=socks&filtered=true",
        "https://www.xroxy.com/free-proxy-lists/",
        "https://www.sslproxies.org/",
        "https://premiumproxy.net/socks-proxy-list"]

        total_proxies = []
        for x in range(len(urls)):
            try:
                request = urllib.request.Request(
                                                    urls[x],
                                                    data=None,
                                                    headers = {
                                                                "User-Agent" : self.getUserAgent()
                                                               }
                                                )

                response = urllib.request.urlopen(request,timeout=5)

                html = response.read().decode("utf-8", errors="ignore")
                response.close()
                [total_proxies.append(x) for x in self.process(html)]
            except Exception as e:
                print("Error", urls[x])
                continue


        return total_proxies