import json
import urllib
import urllib2

from flask import Flask

import shortcuts

app = Flask(__name__)


@app.route("/")
def hello():
    return "hello"

@app.route("/search/<term>")
def search(term):
    url = "https://api.twitter.com/1.1/search/tweets.json?" + urllib.urlencode({
        "q": urllib.quote(term),
        "result_type": "mixed"
    })
    print(url)
    search_req = shortcuts.new_authenticated_request(url)
    search_response = urllib2.urlopen(search_req)
    search_data = json.loads(search_response.read())

    # Build HTML to return
    head_html = "<head><title>Search: " + term + "</title></head>"

    # Processing the tweets themselves
    tweet_html = "<ul>"
    for tweet in search_data["statuses"]:
        tweet_html += "<li>" + tweet["text"] + "</li>"
    tweet_html += "</ul>"

    # Wrapping up the tweet_html into a HTML body with a title
    body_html = "<body><h1>Search: " + term + "</h1>" + tweet_html + "</body>"

    # Join the head and body together
    html = "<html>" + head_html + body_html + "</html>"
        
    return html


if __name__ == "__main__":
    app.run(debug=True)
