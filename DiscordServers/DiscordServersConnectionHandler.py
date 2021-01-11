import urllib, json
from xml.dom import minidom

class DiscordServersConnectionHandler:
    def __init__(self, logger):
        self.logger = logger

    def getServerListingURLArray(self):
        urls = []
        req = urllib.request.Request(
            "https://discordservers.com/sitemap.xml",
             data=None,
             headers={
                    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                    })
        try:
            with urllib.request.urlopen(req) as url:
                data = minidom.parseString(url.read().decode())
                for element in data.getElementsByTagName("sitemap"):
                    url = element.getElementsByTagName("loc")[0].firstChild.nodeValue
                    urls.append(url)
            urls.pop(0)
            return urls
                
        except Exception as e:
            self.logger.commit(2, "DiscordServersConnectionHandler", "getServerListingURLArray", e)

    