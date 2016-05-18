import flask
import shortcuts


tweeter = flask.Flask("Tweeter")


@tweeter.route("/")
def hello():
    return "hello"

@tweeter.route("/search/<term>")
def search(term):
    results = shortcuts.twitter_search(term, 10)

    # Build HTML to return
    head_html = "<head><title>Search: " + term + "</title></head>"

    # Processing the tweets themselves
    tweet_html = "<ul>"
    for tweet in results:
        tweet_html += "<li>" + tweet["text"] + "</li>"
    tweet_html += "</ul>"

    # Wrapping up the tweet_html into a HTML body with a title
    body_html = "<body><h1>Search: " + term + "</h1>" + tweet_html + "</body>"

    # Join the head and body together
    html = "<html>" + head_html + body_html + "</html>"
        
    return html


if __name__ == "__main__":
    tweeter.run(debug=True)
