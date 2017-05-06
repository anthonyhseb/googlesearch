=====
Usage
=====

To use google-search in a project::

    from googlesearch import googlesearch.GoogleSearch
    response = GoogleSearch().search("something")
    for result : response.results:
        print("Title: " + result.title)
        print("URL: " + result.url)
        print("Content: " + result.getText())
        print("Html: " + result.getMarkup())
