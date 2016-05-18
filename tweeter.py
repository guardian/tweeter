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

    # Processing the tweets themselves
    tweet_html = ""
    for tweet in results:
        tweet_html = tweet_html + "<p>" + tweet["text"] + "</p>"

    # Make a HTML title containing the search term
    title_html = "<h1>Tweets containing " + term + "</h1>"

    # Combine these to make the HTML "body"
    body_html = "<body>" + title_html + tweet_html + "</body>"

    # Wrap all this in html tags
    html = "<html>" + body_html + "</html>"
        
    return html


if __name__ == "__main__":
    tweeter.run(debug=True)
