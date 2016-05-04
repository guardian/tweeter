import base64
import json
import urllib
import urllib2


# These are secret values from https://apps.twitter.com
CONSUMER_KEY = "13XVPnFDyaywklg2YZaWFIDkx"
CONSUMER_SECRET = "I2pEsiGrn6rtfKfmywd5f8tQdd1d90u7TuS0FLvikTl3vlTlvR"


# Cached access token
access_token = None


def new_access_token_request():
    '''Create a HTTP request to Twitter to get the access token required for making
    other requests to Twitter's APIs.

    We must use the "consumer key" and "consumer secret" values assigned to our
    app to create a The implementation of this method is based on the
    instructions on this page: https://dev.twitter.com/oauth/application-only

    '''
    # URL-encode the consumer key and consumer secret
    url_safe_consumer_key = urllib.quote(CONSUMER_KEY)
    url_safe_consumer_secret = urllib.quote(CONSUMER_SECRET)

    # Join them together with a colon
    key_and_secret = url_safe_consumer_key + ":" + url_safe_consumer_secret

    # Base 64 encode them
    base_64_key_and_secret = base64.b64encode(key_and_secret)

    # Create a request object from the URL
    request = urllib2.Request("https://api.twitter.com/oauth2/token")

    # Add the value we calculated above as a header of the request
    request.add_header("Authorization", "Basic " + base_64_key_and_secret)

    # Add this other magic key-value pair as body data. This has the side effect
    # of making this into a POST request with the appropriate Content-Type
    # header.
    data = urllib.urlencode({"grant_type": "client_credentials"})
    request.add_data(data)

    return request


def get_access_token():
    '''Make a request to Twitter to get the access token required for making other
    requests and return that token.

    '''
    global access_token
    if not access_token:
        print("Access token not cached, making authentication request...")
        request = new_access_token_request()
        response = urllib2.urlopen(request)
        response_data = json.loads(response.read())
        access_token = response_data["access_token"]
    return access_token


def new_authenticated_request(url):
    '''Return a new Request object for the supplied url, authenticated with the
    supplied access token.

    Get an access token using the get_access_token function.

    '''
    request = urllib2.Request(url)
    request.add_header("Authorization", "Bearer " + get_access_token())
    return request


def twitter_request(url, params):
    full_url = "https://api.twitter.com/1.1/search/tweets.json?" + urllib.urlencode(params)
    print(full_url)
    search_req = new_authenticated_request(full_url)
    search_response = urllib2.urlopen(search_req)
    return json.loads(search_response.read())
