import urllib3
import sys
from bs4 import BeautifulSoup
import time
import requests


def strip_brackets(string):
    """
    remove brackets from a string
    leave brackets between "<>" tags in place
    """
    string = "" + str(string)
    # print "input: ",string
    d = 0
    k = 0
    out = ''
    for i in string:
        # check for <>tag when not in parentheses mode
        if d < 1:
            if i == '>':
                k -= 1

            if i == "<":
                k += 1

        # check for parentheses
        if k < 1:
            if i == '(':
                d += 1

            if d > 0:
                out += ' '
            else:
                out += i

            if i == ')':
                d -= 1
        else:
            out += i

    # print "output: ",out
    return out


class PhilosophyCrawler():

    def __init__(self):
        retry = urllib3.Retry(connect=13, read=2, redirect=5, backoff_factor=0.08)
        self.http = urllib3.PoolManager(num_pools=2, retries=retry)
        self.http.headers.pop("Accept-Encoding", "gzip")
        self.prefix = "http://en.wikipedia.org"
        self.visited = []

    def trace_(self, articleURL):
        name = articleURL.rpartition("/wiki/")[2]
        print(articleURL)
        if self.visited.__contains__(name):
            print("YOU ARE IN A LOOP")
            return "INVALIDCHAIN:loop"
        if not name == "Special:Random":
            self.visited.append(name)

        time.sleep(1)
        r = self.http.request('GET', articleURL+"?maxlag=1")
        soup = BeautifulSoup(r.data, features="html.parser")

        for para in soup.find('div', class_="mw-parser-output").findAll({'ul': True, 'p': True},
                                                                        recursive=False):  # loops each <p>
            para = BeautifulSoup(strip_brackets(para), features="html.parser")  # removes links in brackets
            for link in para.findAll('a'):  # for each <a> in the para
                skip = True
                for val in link.attrs:  # for each attribute in the <a>
                    if val == "href":  # if the current attribute is the href
                        nexturl = link.attrs[val]  # sets the next url
                    if val == "title":  # if current attribute is the title - all wiki links have them
                        nextpagename = link.attrs[val]  # sets the name of the next page
                        skip = False
                if skip:
                    continue
                if nextpagename == "Philosophy":  # if you reached the end
                    print("You have arrived!")
                    return "SUCCESSFULCHAIN"
                else:
                    if not (nexturl.startswith("http://") or nexturl.startswith("https://")):
                        nexturl = self.prefix + nexturl
                    else:  # urls occaisonally switch between wiktionary and wikipedia
                        self.prefix = nexturl.rpartition("/wiki/")[0]
                        # todo redirect to wiki

                    if "(page does not exist)" in nextpagename:
                        return "INVALIDCHAIN:deadlink"
                    return self.trace_(nexturl)
        # except AttributeError:
        #     return "INVALIDCHAIN:AttributeError"

    def beginTrace(self, url):
        failed = False

        self.visited = []
        result = self.trace_(url)

        if result.__contains__("INVALIDCHAIN"):
            print("CHAIN FAILED")
            failed = True
        if failed:
            endpoint = "failed"
        else:
            endpoint = "successful"
            self.visited.append("Philosophy")

        print(result + "\n\n-------------------------------------- \n\n\n")
        data = {'chain': self.visited}
        r = requests.post(url="http://test.noodlewrecker.xyz:3000/crawl/add/"+endpoint, data=data)


if __name__ == "__main__":  # only runs if main file
    crawl = PhilosophyCrawler()
    if len(sys.argv) == 1:
        print("Starting from random")
        while True:
            crawl.beginTrace("http://en.wikipedia.org/wiki/Special:Random")
    else:
        for i in sys.argv[1:]:
            crawl.beginTrace("http://en.wikipedia.org/wiki/" + i)
