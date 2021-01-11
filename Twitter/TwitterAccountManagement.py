import threading, time

class Timer(threading.Thread):
    def __init__(self):
        self.lock = threading.Lock()
        self.max_calls = 15
        self.num_calls = 0
        self.isDead = False
        super(Timer, self).__init__()

    def run(self):
        while(1):
            if (not self.isDead):
                with self.lock:
                    self.num_calls = 0
            else:
                break
            time.sleep(60*15)

    def closeThread(self):
        self.isDead = True

class TwitterAccountManagement:
    def __init__(self):
        self.account_dict = {}
        self.current_index = 0
        self.account_lock = threading.Lock()
        self.readAccounts()

    def addAccount(self, consumer_key, consumer_secret, access_token, token_secret):
        index = len(self.account_dict.keys())
        tmp_dict = {}
        tmp_dict["consumer_key"] = consumer_key.rstrip()
        tmp_dict["consumer_secret"] = consumer_secret.rstrip()
        tmp_dict["access_token"] = access_token.rstrip()
        tmp_dict["token_secret"] = token_secret.rstrip()
        tmp_dict["timer"] = Timer()
        self.account_dict[index] = tmp_dict

    def getAccount(self):
        account = None
        if (self.current_index == len(self.account_dict.keys())):
            self.current_index = 0

        with self.account_lock:
            account = self.account_dict[self.current_index]
            self.current_index += 1

        return account

    def readAccounts(self):
        with open("TWITTER_ACCOUNTS.csv") as f:
            first_line = True
            for line in f:
                if (not first_line):
                    credentials = line.split(",")
                    self.addAccount(credentials[0],credentials[1],credentials[2],credentials[3])
                first_line = False