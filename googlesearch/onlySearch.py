from googlesearch import GoogleSearch

res = GoogleSearch().search("rakeshsagalagatte")
for result in res.results:
    print("Title: " + result.title)
    print("Content: " + result.getText())