# Contributors:
# https://github.com/anthonyhseb
# https://github.com/rakeshsagalagatte
# https://github.com/hildogjr

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
from pkg_resources import resource_filename
from contextlib import closing

class GoogleSearch:
    with open(resource_filename('googlesearch', 'browser_agents.txt'), 'r') as file_handle:
        USER_AGENTS = file_handle.read().splitlines()
    SEARCH_URL = "https://google.com/search"
    RESULT_SELECTOR = "div.g"
    RESULT_SELECTOR_PAGE1 = "div.g>div>div[id][data-ved]"
    TOTAL_SELECTOR = "#result-stats"
    RESULTS_PER_PAGE = 10
    DEFAULT_HEADERS = [
            ('User-Agent', choice(USER_AGENTS)),
            ("Accept-Language", "en-US,en;q=0.5"),
        ]

    def search(self,
               query,
               num_results = 10,
               prefetch_pages = True,
               num_prefetch_threads = 10):
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
        thread_pool = None
        if prefetch_pages:
            thread_pool = ThreadPool(num_prefetch_threads)
        for i in range(pages) :
            start = i * GoogleSearch.RESULTS_PER_PAGE
            opener = urllib.build_opener()
            opener.addheaders = GoogleSearch.DEFAULT_HEADERS
            with closing(opener.open(GoogleSearch.SEARCH_URL +
                             "?hl=en&q="+ urllib.quote(query) +
                             ("" if start == 0 else
                              ("&start=" + str(start))))) as response:
                soup = BeautifulSoup(response.read(), "lxml")
            if total is None:
                if sys.version_info[0] > 2:
                    totalText = soup.select(GoogleSearch.TOTAL_SELECTOR)[0].children.__next__()
                else:
                    totalText = soup.select(GoogleSearch.TOTAL_SELECTOR)[0].children.next()
                total = int(re.sub("[', ]", "",
                                   re.search("(([0-9]+[', ])*[0-9]+)",
                                             totalText).group(1)))
            selector = GoogleSearch.RESULT_SELECTOR_PAGE1 if i == 0 else GoogleSearch.RESULT_SELECTOR
            self.results = self.parse_results(soup.select(selector), i)
            # if len(search_results) + len(self.results) > num_results:
            #     del self.results[num_results - len(search_results):]
            search_results += self.results
            if prefetch_pages:
                thread_pool.map_async(SearchResult.get_text, self.results)
        if prefetch_pages:
            thread_pool.close()
            thread_pool.join()
        return SearchResponse(search_results, total)

    def parse_results(self, results, page):
        search_results = []
        for result in results:
            if page == 0:
                result = result.parent
            else:
                result = result.find("div")
            h3 = result.find("h3")
            if h3 is None:
                continue
            url = h3.parent["href"]
            title = h3.text
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
            for junk in soup(['style', 'script', 'head', 'title', 'meta']):
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
    num_results = 10
    print ("Fetching first " + str(num_results) + " results for \"" + query + "\"...")
    response = search.search(query, num_results, prefetch_pages=True)
    print ("TOTAL: " + str(response.total) + " RESULTS")
    for count, result in enumerate(response.results):
        print("RESULT #" + str (count+1) + ":")
        print((result._SearchResult__text.strip()
               if result._SearchResult__text is not None else "[None]") + "\n\n")
