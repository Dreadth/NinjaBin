import re
import time
import json
import urllib
import urllib2
import os
import datetime


class NinjaBin:
    def __init__(self):
        self.keys = []
        self.pb = ""
        self.limit = 35
        self.url = "https://scrape.pastebin.com/api_scraping.php"
        self.values = {'limit': self.limit}
        self.url_values = urllib.urlencode(self.values)
        self.fetch_count = 0
        self.check_values = ['zyxel', 'calix', 'pubg', 'dota2']

        self.full_url = self.url + '?' + self.url_values
        self.now = datetime.datetime.now()

    def fetch_data(self):
        while True:
            try:
                self.pb = urllib2.urlopen(self.full_url)
            except urllib2.HTTPError, e:
                print e

            data = json.load(self.pb)
            self.keys = self.keys[:self.limit]
            count = 0
            key_count = 0

            for paste in data:
                if paste['key'] in self.keys:
                    key_count += 1
                    continue
                self.keys.insert(0, paste['key'])
                scrape = urllib2.urlopen(paste['scrape_url'])
                scrape_data = scrape.read()
                count += 1
                self.fetch_count += 1
                i = 0
                while i != len(self.check_values):
                    check_value = self.check_data(scrape_data, self.check_values[i])
                    if check_value is not None:
                        self.dir_creation(check_value)
                        self.data_creation(check_value, paste, scrape_data)
                    i += 1
            print 'Prevented Re-Fetch: ' + str(key_count)
            print 'Fetched This Round: ' + str(count)
            print 'Fetched Total: ' + str(self.fetch_count)
            print 'Key Array Length: ' + str(len(self.keys))
            print '[ ] sleeping 60 ------------------------- - - -'
            time.sleep(60)

    def data_creation(self, check_value, paste, scrape_data):
        if check_value is not None:
            self.dir_creation(check_value)
            filename = "scrape/" + check_value + "/" + self.now.strftime("%Y-%m-%d-") + paste['key'] + ".txt"
            print "[+] Data found in %s -- saving to %s" % \
                  (paste['full_url'], filename)

            data_file = open(filename, 'w')

            data_file.write(scrape_data)
            data_file.close()

    @staticmethod
    def check_data(data, check):
        if check.lower() in data.lower():
            return check.lower()
        return None

    @staticmethod
    def dir_creation(directory):
        if not os.path.exists("scrape/" + directory):
            os.makedirs("scrape/" + directory)


if __name__ == "__main__":
    glitch = NinjaBin()
    glitch.fetch_data()
