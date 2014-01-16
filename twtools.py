import optparse
import requests
from requests_oauthlib import OAuth1
import json

from settings import *

client_error_codes = (400, 401, 403, 404, 410, 420, 429)
server_error_codes = (500, 502, 503, 504)


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


def unblock(args):
    " unblocks all blocked users or only the user_ids, if passed "
    if args:
        unblock_ids(args.split(','))
    else:
        url = TWITTER_API_PREFIX + 'blocks/ids.json'
        oauth = get_oauth()
        response = requests.get(url, params={"stringify_ids": True}, auth=oauth)
        if response.status_code == 200:
            user_ids = json.loads(response.content)[u"ids"]
            print "Unblocking these:", user_ids
            unblock_ids(user_ids)
        else:
            print "Failed fetching blocked ids:"
            print "status_code", response.status_code
            print "response content", dump_json(response.content)


def unblock_ids(ids):
    " unblocks ids "
    url = TWITTER_API_PREFIX + 'blocks/destroy.json'

    error_count = 0
    oauth = get_oauth()
    for user_id in ids:
        params = {"user_id" :user_id, "include_entities": False, "skip_status": True}
        response = requests.post(url=url, params=params, auth=oauth)
        if response.status_code == 200:
            print "Unblocked user:", user_id
        else:
            error_count += 1
            if response.status_code in client_error_codes:
                print "Client error", response.status_code
                print "response content", dump_json(response.content)
            elif response.status_code in server_error_codes:
                print "Twitter API server error", response.status_code
                print "response content", dump_json(response.content)
            if error_count > ERROR_LIMIT:
                raise Exception("Too many errors. Let's take a break for now..")


if __name__ == '__main__':
    cmdparser = optparse.OptionParser()
    cmdparser.add_option("-v", "--verify", action="store_true",
                         dest="verify", default=False,
                         help="Verify auth credentials.")
    cmdparser.add_option("-u", "--unblock", action="store_true",
                         dest="unblock", default=False,
                         help="Unblocks user_ids(csv) passed or all blocked users.")

    (options, args) = cmdparser.parse_args()

    if options.verify:
        verify_credentials()
    if options.unblock:
        unblock(args)
