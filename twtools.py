import optparse
import requests
from requests_oauthlib import OAuth1
import json

from settings import *


def get_oauth():
    " Get oauth object "
    return OAuth1(TWITTER_CONF.get('consumer_key'), TWITTER_CONF.get('consumer_secret'),
                      resource_owner_key=TWITTER_CONF.get('access_token'), resource_owner_secret=TWITTER_CONF.get('access_token_secret'))


def dump_json(string_data):
    " dump json data "
    return json.dumps(json.loads(string_data), indent=2)


def verify_credentials():
    " verify auth credentials "
    url = TWITTER_API_PREFIX + 'account/verify_credentials.json'

    oauth = get_oauth()
    response = requests.get(url=url, auth=oauth)
    if response.status_code == 200:
        print "Verified auth credentials:"
        print dump_json(response.content)
    else:
        print "Auth verification failed:"
        print "status_code", response.status_code
        print "response content", dump_json(response.content)


if __name__ == '__main__':
    cmdparser = optparse.OptionParser()
    cmdparser.add_option("-v", "--verify", action="store_true",
                         dest="verify", default=False,
                         help="Verify auth credentials.")

    (options, args) = cmdparser.parse_args()

    if options.verify:
        verify_credentials()