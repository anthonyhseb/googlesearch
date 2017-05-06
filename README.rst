=============
google-search
=============


.. image:: https://img.shields.io/pypi/v/googlesearch.svg
        :target: https://pypi.python.org/pypi/googlesearch

.. image:: https://img.shields.io/travis/anthonyhseb/googlesearch.svg
        :target: https://travis-ci.org/anthonyhseb/googlesearch

.. image:: https://readthedocs.org/projects/googlesearch/badge/?version=latest
        :target: https://googlesearch.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/anthonyhseb/googlesearch/shield.svg
     :target: https://pyup.io/repos/github/anthonyhseb/googlesearch/
     :alt: Updates


Library for scraping google search results.

Usage:

from googlesearch import googlesearch.GoogleSearch
response = GoogleSearch().search("something")
for result : response.results:
	print("Title: " + result.title)
	print("Content: " + result.getText())



* Free software: MIT license
* Documentation: https://googlesearch.readthedocs.io.


Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

