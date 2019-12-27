'''
Created on May 6, 2017

@author: anthony
'''
import unittest
from googlesearch.googlesearch import GoogleSearch

class TestGoolgeSearch(unittest.TestCase):

    def test_search(self):
        num_results = 15
        response = GoogleSearch().search("unittest", num_results = num_results)
        self.assertTrue(response.total > 1000, "repsonse.total is way too low")
        self.assertTrue(len(response.results) == 15, "number of results is " + str(len(response.results)) + " instead of " + str(num_results))
        for result in response.results:
            self.assertTrue(result.getText() is not None, "result.text is None")

if __name__ == '__main__':
    unittest.main()