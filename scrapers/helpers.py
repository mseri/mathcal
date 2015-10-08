# -*- encoding: utf-8 -*-
"""Helper class for the London Maths Events backend.

It provides: REF_ZERO_DATE, EMPTY_CACHE and the function
jsonify_seminars(url, getEventList, isJson=False, last_update=None).

The events in the list returned by getEventList are of the form:
{
  'start': DateTime,
  'end': DateTime,
  'title': String,
  'description': String,
  'location': String
}
"""

import calendar
from datetime import datetime
from dateutil.parser import parse
import json
from time import time

from bs4 import BeautifulSoup

import requests


# pylint: disable=E1101
REQ_OK = requests.codes.ok
REF_ZERO_DATE = datetime(1970, 1, 1)
EMPTY_CACHE = json.dumps([])


#########################################################
def get_raw(url, last_update):
    """Takes an url and an optional CachedResult instance and returns an
    None (in case the cache is current or there is some error) or the
    raw data content, decded in utf-8 with ignored errors."""

    # with a streamed request we can analyse the headers and avoid
    # to get the content unless we need it
    req = requests.get(url, stream=True)

    if req.status_code != REQ_OK:
        print("ERROR: status code %d while requesting %s" % (req.status_code, url))
        return None

    last_modified = req.headers.get("last-modified")
    if last_modified and last_update and timestamp(parse(last_modified)) <= timestamp(last_update):
        print("INFO: cache still current, skipping download of %s" % url)
        return None

    return req.content.decode("utf-8", "ignore")


#########################################################
def tAdjust(sTime):
    """Takes a string representing time. If it has only one/two
    digit adds ':00' otherwise it only replaces the '.' separator
    between hours and minutes with ':'. Returns the modified string."""
    if len(sTime) <= 2:
        return sTime + ":00"

    return sTime.replace('.', ':')


#########################################################
class CachedObject:
    def __init__(self, cache=None):
        if cache:
            self.cache(cache)
        else:
            self._cache = EMPTY_CACHE
            self._last_update = REF_ZERO_DATE

    @property
    def cache(self):
        return self._cache

    @cache.setter
    def cache(self, cache):
        self._cache = cache
        self._last_update = datetime.now().replace(tzinfo=None)

    @property
    def last_update(self):
        return self._last_update


def expired(date_, ttl=60000):
    return timestamp(date_) + ttl < time()


#########################################################
# http://stackoverflow.com/questions/455580/json-datetime-between-python-and-javascript
def jsonDateTimeHandler(obj):
    """Takes an object and tries to serialize it in JSON
    by using strftime or isoformat."""
    if hasattr(obj, "strftime"):
        # To avoid problems with the js date-time format
        return obj.strftime("%a %b %d, %Y %I:%M %p")
    elif hasattr(obj, 'isoformat'):
        return obj.isoformat()
    # elif isinstance(obj, ...):
    #     return ...
    else:
        raise TypeError(
            'Object of type %s with value of %s is not JSON serializable' %
            (type(obj), repr(obj)))


#########################################################

def timestamp(datetime_obj):
    """Returns the unix timestamp of datetime_obj.
    """
    return calendar.timegm(datetime_obj.utctimetuple())


#########################################################

def jsonify_seminars(url, get_event_list, isJson=False, last_update=None):
    """Process the data obtained from url and returns a json dump
    of the updated list of event.

    The data is parsed with BeautifulSoup (or json.loads if isJson is true)
    and elaborated by the function getEventList.

    An optional last_update (datetime object) parameter allows to check if the
    cache is current by comparison with the url request headers.
    """

    rawdata = get_raw(url, last_update)

    # if we have new rawdata we proceed with the elaboration
    # otherwise (errors or current cache), we revert to the cache
    if rawdata:
        print("INFO: JSONification of ", url)
        if isJson:
            data = json.loads(rawdata)
        else:
            data = BeautifulSoup(rawdata, "html.parser") #"html5lib"

        event_list = get_event_list(data)
        return json.dumps(list(event_list), default=jsonDateTimeHandler)
    else:
        return EMPTY_CACHE
