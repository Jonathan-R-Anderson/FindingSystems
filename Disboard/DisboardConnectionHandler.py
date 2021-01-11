import urllib, re

class DisboardConnectionHandler:
    def __init__(self, logger):
        self.logger = logger
        self.base_url = "https://disboard.org/servers/"
        self.page_count = 1
        self.sort_by_url = "?sort=-member_count"

    def getNumberOfServers(self):
        try:
            req = urllib.request.Request(
                "https://disboard.org/servers",
                data=None,
                headers={
                    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                    })
            with urllib.request.urlopen(req) as url:
                data = url.read().decode()
                number_servers_raw = re.search(r'<strong>(.*?)</strong>', data).group(1)
                number_servers = int(number_servers_raw.split(" ")[0])
                return number_servers
        except Exception as e:
            print("error", e)
            self.logger.commit(2, "DisboardConnectionHandler", "getNumberOfServers", e)

    def getResultsPerPage(self):
        try:
            req = urllib.request.Request(
                "https://disboard.org/servers",
                data=None,
                headers={
                    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                    })
            with urllib.request.urlopen(req) as url:
                data = url.read().decode()
                results_per_page_raw = re.search(r'Showing <b>(.*?)</b> of', data).group(1)
                results_per_page = int(results_per_page_raw.split("<b>")[1])
                return results_per_page
        except Exception as e:
            print("error", e)
            self.logger.commit(2, "DisboardConnectionHandler", "getResultsPerPage", e)


    def getNumberOfPages(self):
        number_servers = self.getNumberOfServers()
        results_per_page = self.getResultsPerPage()
        total_page_calls = 0
        while(number_servers > 0):
            total_page_calls += 1
            number_servers -= results_per_page
        return total_page_calls

    def getServersMetaData(self):
        number_of_pages = self.getNumberOfPages()
        server_listing = [] # (number of users,discord url)
        while(number_of_pages > 0):
            try:
                req = urllib.request.Request(
                    self.base_url+str(number_of_pages)+self.sort_by_url,
                    data=None,
                    headers={
                    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                        })
                with urllib.request.urlopen(req) as url:
                    data = url.read().decode()
                    #server_raw = re.findall(r'column is-one-third-desktop is-half-tablet(.*?)<', data)
                    server_raw = re.findall(r'column is-one-third-desktop is-half-tablet(.*?)<!-- .server -->', data, re.MULTILINE | re.DOTALL)
                    server_listing = []
                    for entry in server_raw:
                        entry = re.search(r'<div class=\"server-join\">(.*?)class=\"', entry, re.MULTILINE | re.DOTALL).group(1)
                        print(entry)
                        break
                    break

            except Exception as e:
                print("error", e)
                self.logger.commit(2, "DisboardConnectionHandler", "getServersMetaData", e)
            number_of_pages -= 1


    def getTopServers(self):
        # if 2 standard deviations below the most popular server do not include
        # get all servers member counts
        pass
