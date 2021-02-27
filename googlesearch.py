# Original projet from https://github.com/anthonyhseb/googlesearch under MIT License.
# Created on May 5, 2017 by @anthony
# Code updated for @rakeshsagalagatte on https://github.com/rakeshsagalagatte/googlesearch.
# More fix and improvements by Hildo Guillardi Júnior on https://github.com/hildogjr/googlesearch.

import sys
if sys.version_info[0] > 2:
    import urllib.request as urllib
else:
    import urllib2 as urllib
import math
import re
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool  # To deal with the parallel scrape.
from random import choice
from time import sleep
        
class GoogleSearch:
    with open('browser_agents.txt', 'r') as file_handle:
        USER_AGENTS = file_handle.read().splitlines()
    SEARCH_URL = "https://google.com/search"
    RESULT_SELECTOR = "h3.r a"
    TOTAL_SELECTOR = "#result-stats"
    RESULTS_PER_PAGE = 10
    DEFAULT_HEADERS = [
            ('User-Agent', choice(USER_AGENTS)),
            ("Accept-Language", "en-US,en;q=0.5"),
        ]
    
    def search(self,
               query: str,
               num_results: int = 10,
               prefetch_pages: bool = True,
               qty_prefetch_threads: int = 10,
               time_between_threads: float = 2.5):
        '''Perform the Google search.

        Parameters:
            String to search.
            Minimum number of result to stop search.
            Prefetch answered pages.
            Number of threads used t prefetch the pages.
            Time between thread executions in second to void IP block.
        '''
        search_results = []
        pages = int(math.ceil(num_results / float(GoogleSearch.RESULTS_PER_PAGE)))
        total = None
        for i in range(pages) :
            start = i * GoogleSearch.RESULTS_PER_PAGE
            opener = urllib.build_opener()
            opener.addheaders = GoogleSearch.DEFAULT_HEADERS
            with opener.open(GoogleSearch.SEARCH_URL +
                             "?q="+ urllib.quote(query) +
                             ("" if start == 0 else
                              ("&start=" + str(start)))) as response:
                soup = BeautifulSoup(response.read(), "lxml")
            if total is None:
                if sys.version_info[0] > 2:
                    totalText = soup.select(GoogleSearch.TOTAL_SELECTOR)[0].children.__next__()
                else:
                    totalText = soup.select(GoogleSearch.TOTAL_SELECTOR)[0].children.next()
                total = int(re.sub("[', ]", "",
                                   re.search("(([0-9]+[', ])*[0-9]+)",
                                             totalText).group(1)))
            self.results = self.parse_results(soup.select(GoogleSearch.RESULT_SELECTOR))
            # if len(search_results) + len(self.results) > num_results:
            #     del self.results[num_results - len(search_results):]
            search_results += self.results
            if prefetch_pages:
                thread_pool = ThreadPool(qty_prefetch_threads)
                for r in self.results:
                    def local_fun():
                        r.get_text()
                        sleep(time_between_threads)
                    thread_pool.apply_async(func=local_fun)
                thread_pool.close()
                thread_pool.join()
        return SearchResponse(search_results, total)
        
    def parse_results(self, results):
        search_results = []
        for result in results:
            url = result["href"]
            title = result.text
            search_results.append(SearchResult(title, url))
        return search_results

class SearchResponse:
    def __init__(self, results, total):
        self.results = results
        self.total = total

class SearchResult:
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.__text = None
        self.__markup = None
    
    def get_text(self):
        if self.__text is None:
            soup = BeautifulSoup(self.get_markup(), "lxml")
            for junk in soup(["script", "style"]):
                junk.extract()
                self.__text = soup.get_text()
        return self.__text
    
    def get_markup(self):
        if self.__markup is None:
            opener = urllib.build_opener()
            opener.addheaders = GoogleSearch.DEFAULT_HEADERS
            response = opener.open(self.url)
            self.__markup = response.read()
        return self.__markup
    
    def __str__(self):
        return  str(self.__dict__)
    def __unicode__(self):
        return str(self.__str__())
    def __repr__(self):
        return self.__str__()


# Main entry for test and external script use.
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:  # Only the file name.
        query = "python"
    else:
        query = " ".join(sys.argv[1:])
    search = GoogleSearch()
    qty = 10
    print ("Fetching first " + str(qty) + " results for \"" + query + "\"...")
    response = search.search(query, qty, prefetch_pages=True)
    print ("TOTAL: " + str(response.total) + " RESULTS")
    for count, result in enumerate(response.results):
        print("RESULT #" + str (count+1) + ":")
        print((result._SearchResult__text.strip()
               if result._SearchResult__text is not None else "[None]") + "\n\n")
