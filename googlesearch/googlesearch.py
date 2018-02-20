'''
Created on May 5, 2017

@author: anthony
'''
##compact

import sys
if sys.version_info < (3,):
    import urllib2
else:
    import urllib
    import urllib.request
    import urllib.parse
import math
import re
from bs4 import BeautifulSoup
from threading import Thread
from collections import deque
from time import sleep
from unidecode import unidecode


        
class GoogleSearch:
    USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 58.0.3029.81 Safari/537.36"
    SEARCH_URL = "https://google.com/search"
    RESULT_SELECTOR = "h3.r a"
    TOTAL_SELECTOR = "#resultStats"
    RESULTS_PER_PAGE = 10
    DEFAULT_HEADERS = [
            ('User-Agent', USER_AGENT),
            ("Accept-Language", "en-US,en;q=0.5"),
        ]
    
    def search(self, query, as_epq = None, as_oq= None, as_eq = None, filetype = None, site = None, as_qdr = None, intitle = None, inurl = None,
        as_rq = None, as_lq = None, lr = None, cr = 0, hl = None, num_results = 10, prefetch_pages = True, prefetch_threads = 1):
        '''
        Query Google returning a SearchResult object.

        Keyword arguments:
        query: The search query (required)
        as_epq: Force the search to include the text. Useful for search filters to include the given text. Uses AND filter.
        as_oq:  Force the search to include the text. More advanced version of the one above but using the OR filter.
        as_eq: Force the search to exclude the text. Results must NOT include any words in this string.
        filetype: Only returns results that end in .text. Eg to get pdf files simply put filetype= pdf
        site: Force the search to include results from a given site. ie Limits results to just the site you choose.
        as_qdr: Limit the search results to include theresult included from the given time.
        intitle: Force the seach to include the text in the title.
        inurl: Force the seach to include the text in the url.
        as_rq: Finds sites Google thinks are related to the URL you put in.
        as_lq: Finds sites that link to the URL you put in.
        lr: Limits the languages used to return results. Not hugely effective.
        cr: Limits the search results to pages/sites from certain locations. Default 0 for your home country.
            Change it to include results from another country
        hl: Interface language.
        num_results: Maxximum numer of results to be searched. Use lower number to get faster results. (Default value= 10)
        prefetch_pages: By default the result URLs are fetched eagerly when the search request is made. (Default value= True)
                        Fetching can be deferred until searchResult.getText() or getMarkup() are called by passing prefetch_results = False
        prefetch_threads: Only works when prefetch_results= True. (Default value= 1)
                         Searches the queries in seperate threads. For best results set to the maximum number your processor supports.
                         For optimum reasons it will reset it to the number of processor cores if it is 1.

        Returns:
        A SearchResult object
        '''
        searchResults = []
        if prefetch_threads==1:
            import psutil
            prefetch_threads = psutil.cpu_count()
        if sys.version_info < (3,):
            squery = urllib2.quote(query) + ("" if intitle==None else ("+&intitle%3A\"" + urllib2.quote(intitle) + "\"")) + \
                ("" if intitle==None else ("+&inurl%3A\"" + urllib2.quote(inurl) + "\""))  + ("" if site==None else ("&+site%3A\"" + urllib2.quote(site) + "\""))
        else:
            squery = urllib.parse.quote(query) + ("" if intitle==None else ("+&intitle%3A\"" + urllib.parse.quote(intitle) + "\"")) + \
                ("" if inurl==None else ("+&inurl%3A\"" + urllib.parse.quote(inurl) + "\"")) + ("" if site==None else ("&+site%3A\"" + urllib.parse.quote(site) + "\""))
        pages = int(math.ceil(num_results / float(GoogleSearch.RESULTS_PER_PAGE)))
        fetcher_threads = deque([])
        total = None;
        for i in range(pages) :
            startp = i * GoogleSearch.RESULTS_PER_PAGE
            if sys.version_info < (3,):
                opener = urllib2.build_opener()
                opener.addheaders = GoogleSearch.DEFAULT_HEADERS
                response = opener.open(GoogleSearch.SEARCH_URL + "?q="+ squery + ("" if as_epq==None else ("&as_epq=" + urllib2.quote(as_epq))) + \
                    ("" if as_oq==None else ("&as_oq=" + urllib2.quote(as_oq))) + ("" if as_eq==None else ("&as_eq=" + urllib2.quote(as_eq))) + \
                    ("" if filetype==None else ("&as_filetype=" + urllib2.quote(filetype))) + ("" if startp == 0 else ("&start=" + str(startp))) + \
                    ("" if as_qdr==None else ("&as_qdr=" + urllib2.quote(as_qdr))) + ("" if as_rq==None else ("&as_rq=" + urllib2.quote(as_rq))) + \
                    ("" if as_lq==None else ("&as_lq=" + urllib2.quote(as_lq))) + ("" if hl==None else ("&hl=" + urllib2.quote(hl))) + "&cr=" + str(cr))
            else:
                opener = urllib.request.build_opener()
                opener.addheaders = GoogleSearch.DEFAULT_HEADERS
                response = opener.open(GoogleSearch.SEARCH_URL + "?q="+ squery + ("" if as_epq==None else ("&as_epq=" + urllib.parse.quote(as_epq))) + \
                    ("" if as_oq==None else ("&as_oq=" + urllib.parse.quote(as_oq))) + ("" if as_eq==None else ("&as_eq=" + urllib.parse.quote(as_eq))) + \
                    ("" if filetype==None else ("&as_filetype=" + urllib.parse.quote(filetype))) + ("" if startp == 0 else ("&start=" + str(startp))) + \
                    ("" if as_qdr==None else ("&as_qdr=" + urllib.parse.quote(as_qdr))) + ("" if as_rq==None else ("&as_rq=" + urllib.parse.quote(as_rq))) + \
                    ("" if as_lq==None else ("&as_lq=" + urllib.parse.quote(as_lq))) + ("" if hl==None else ("&hl=" + urllib.parse.quote(hl))) + "&cr=" + str(cr))
                #response = opener.open(surl)
            soup = BeautifulSoup(response.read(), "lxml")
            response.close()
            if total is None:
                if sys.version_info < (3,):
                    totalText = soup.select(GoogleSearch.TOTAL_SELECTOR)[0].children.next().encode('utf-8')
                    total = int(re.sub("[', ]", "", re.search("(([0-9]+[', ])*[0-9]+)", totalText).group(1)))
                else:
                    totalText = soup.select(GoogleSearch.TOTAL_SELECTOR)[0].children.__next__().encode('utf-8')
                    ch1 = soup.select(GoogleSearch.TOTAL_SELECTOR)[0].children
                    totalText = soup.select(GoogleSearch.TOTAL_SELECTOR)[0].children.__next__().encode('utf-8')
                    r1 = re.search(b"(([0-9]+[',\. ])*[0-9]+)", totalText)
                    total = int(re.sub(b"[',\. ]", b"", r1.group(1)))
            results = self.parseResults(soup.select(GoogleSearch.RESULT_SELECTOR))
            if len(searchResults) + len(results) > num_results:
                del results[num_results - len(searchResults):]
            searchResults += results
            if prefetch_pages:
                for result in results:
                    while True:
                        running = 0
                        for thread in fetcher_threads:
                            if thread.is_alive():
                                running += 1
                        if running < prefetch_threads:
                            break
                        sleep(1)
                    fetcher_thread = Thread(target=result.getText)
                    fetcher_thread.start()
                    fetcher_threads.append(fetcher_thread)
        for thread in fetcher_threads:
            thread.join()
        return SearchResponse(searchResults, total);
        
    def parseResults(self, results):
        searchResults = [];
        for result in results:
            url = result["href"];
            title = result.text
            searchResults.append(SearchResult(title, url))
        return searchResults

class SearchResponse:
    def __init__(self, results, total):
        self.results = results;
        self.total = total;

class SearchResult:
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.__text = None
        self.__markup = None
    
    def getText(self):
        if self.__text is None:
            soup = BeautifulSoup(self.getMarkup(), "lxml")
            for junk in soup(["script", "style"]):
                junk.extract()
                self.__text = unidecode(soup.get_text())
        return self.__text
    
    def getMarkup(self):
        if self.__markup is None:
            if sys.version_info < (3,):
                opener = urllib2.build_opener()
            else:
                opener = urllib.request.build_opener()
            opener.addheaders = GoogleSearch.DEFAULT_HEADERS
            response = opener.open(self.url);
            self.__markup = response.read()
        return self.__markup
    
    def __str__(self):
        return  str(self.__dict__)
    def __unicode__(self):
        return unicode(self.__str__())
    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    search = GoogleSearch()
    i=1
    query = " ".join(sys.argv[1:])
    if len(query) == 0:
        query = "python"
    count = 10
    print ("Fetching first " + str(count) + " results for \"" + query + "\"...")
    response = search.search(query, count)
    print ("TOTAL: " + str(response.total) + " RESULTS")
    for result in response.results:
        print("RESULT #" +str (i) + ": "+ (result._SearchResult__text if result._SearchResult__text is not None else "[None]") + "\n\n")
        i+=1
