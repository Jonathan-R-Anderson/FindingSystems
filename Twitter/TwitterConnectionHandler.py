import tweepy, time
class TwitterConnectionHandler:
    def __init__(self, twitteraccountmanagement):
        self.twitteraccountmanagement = twitteraccountmanagement
        self.api = self.getAPI()
        self.account_dict = self.twitteraccountmanagement.getAccount()

    def getAPI(self):
        self.account_dict = self.twitteraccountmanagement.getAccount()
        auth = tweepy.OAuthHandler(self.account_dict["consumer_key"], self.account_dict["consumer_secret"])
        auth.set_access_token(self.account_dict["access_token"], self.account_dict["token_secret"])
        return tweepy.API(auth)

    def checkHowManyAccountsLoggedIn(self):
        count = 0

        keys = []
        for key in self.twitteraccountmanagement.account_dict.keys():
            keys.append(int(key))

        for i in range(0, max(keys)):
            try:
                time.sleep(3)
                print("trying", i)
                print(self.api.me())
                count += 1
                self.api = self.getAPI()
            except Exception as e:
                pass
        return count

    def getStartingID(self, query):
        while(1):
            try:
                tmp_timer = self.account_dict["timer"]
                with tmp_timer.lock:
                    if (tmp_timer.num_calls < tmp_timer.max_calls):
                        tmp_timer.num_calls += 1
                        search_query = self.api.search(q=query, count=1)
                        if (len(search_query) > 0):
                            return search_query[0].id
                        else:
                            print("search query error", search_query)
                    else:
                        print("calls maxed out, changing accounts")
                        self.api = self.getAPI()
            except Exception as e:
                if ("Sorry, that page does not exist." in str(e)):
                    return None
                elif ("Rate limit exceeded" in str(e)):
                    print("switching accounts")
                    self.api = self.getAPI()
                elif ("Could not authenticate you" in str(e)):
                    print("Error, could not authenticate", self.twitteraccountmanagement.account_dict[self.twitteraccountmanagement.current_index])
                    self.api = self.getAPI()
                elif ("To protect our users from spam and other malicious activity" in str(e)):
                    print("Account flagged, log into", self.twitteraccountmanagement.account_dict[self.twitteraccountmanagement.current_index])
                    self.api = self.getAPI()
                else:
                    print("ERROR in TwitterConnectionHandler.getStartingID", e)

                time.sleep(3)

    def getTrends(self, woeid):
        while(1):
            try:
                tmp_timer = self.account_dict["timer"] 
                with tmp_timer.lock:
                    if (tmp_timer.num_calls < tmp_timer.max_calls):
                        tmp_timer.num_calls += 1
                        return self.api.trends_place(woeid)
                    else:
                        print("calls maxed out, changing accounts")
                        self.api = self.getAPI()
            except Exception as e:
                if ("Sorry, that page does not exist." in str(e)):
                    return None
                elif ("Rate limit exceeded" in str(e)):
                    print("switching accounts")
                    self.api = self.getAPI()
                elif ("Could not authenticate you" in str(e)):
                    print("Error, could not authenticate", self.twitteraccountmanagement.account_dict[self.twitteraccountmanagement.current_index])
                    self.api = self.getAPI()
                elif ("To protect our users from spam and other malicious activity" in str(e)):
                    print("Account flagged, log into", self.twitteraccountmanagement.account_dict[self.twitteraccountmanagement.current_index])
                    self.api = self.getAPI()
                else:
                    print("ERROR in TwitterConnectionHandler.getTrends()", e)

                time.sleep(3)

    def generateCountryWOEIDArray(self):
        import yweather, pycountry
        country_name_array = [country.name for country in pycountry.countries]
        yweather_client = yweather.Client()
        woeids = []
        for country in country_name_array:
            try:
                woeid = yweather_client.fetch_woeid(country)
                woeids.append(woeid)
            except Exception as e:
                print("Error in generateCountryWOEIDArray", e)
        return woeids