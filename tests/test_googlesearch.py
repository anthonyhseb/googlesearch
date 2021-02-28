'''
Created on May 6, 2017

@author: anthony
'''
import unittest
from googlesearch.googlesearch import GoogleSearch

class TestGoolgeSearch(unittest.TestCase):

    def test_search(self):
        num_results = 15
        min_results = 11
        max_results = 20
        response = GoogleSearch().search("unittest", num_results = num_results)
        self.assertTrue(response.total > 1000, "repsonse.total is way too low")
        self.assertTrue(len(response.results) >= min_results, "number of results is " + str(len(response.results)) + ", expected at least " + str(min_results))
        self.assertTrue(len(response.results) <= max_results, "number of results is " + str(len(response.results)) + ", expected at most " + str(max_results))
        for result in response.results:
            self.assertTrue(result.url is not None, "result.url is None")
            self.assertTrue(result.url.startswith("http"), "result.url is invalid: " + result.url)
        for result in response.results:
            self.assertTrue(result.get_text() is not None, "result.text is None")

if __name__ == '__main__':
    unittest.main()
