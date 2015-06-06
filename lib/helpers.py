# -*- encoding: utf-8 -*-
"""Helper class for the London Maths Events backend.

It provides: requests, re, bs4.BeautifulSoup, bs4.NavigableString, bs4.Tag,
dateutil.parser.parse, dateutil.relativedelta.relativedelta, datetime.date,
datetime.datetime, json and the function 
jsonifySeminars(url, getEventList, cached, cacheStillCurrent=None, isJson=False).

The events in the list returned by getEventList are of the form:
{
  'start': DateTime,
  'end': DateTime,
  'title': String,
  'description': String,
  'location': String
}
"""

import requests
import re

from bs4 import BeautifulSoup, NavigableString, Tag

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from datetime import date, datetime

import json

# pylint: disable=E1101
REQ_OK = requests.codes.ok
REF_ZERO_DATE = datetime(1970, 1, 1)


#########################################################
def getRawData(url, cached=None):
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
  if (last_modified and cached and relativedelta(parse(last_modified).replace(
      tzinfo=None), cached.last_updated).days < 0):
    print("INFO: cache still current, skipping download of %s" % (url))
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
class CachedResult:
  # no docstring here... 
  # the caching will be completely refactored (if I find some spare time)
  def __init__(self):
    self.cache = json.dumps([])
    self.last_updated = REF_ZERO_DATE

  def update(self, cache):
    self.cache = cache
    self.last_updated = datetime.now().replace(tzinfo=None)


#########################################################
# http://stackoverflow.com/questions/455580/json-datetime-between-python-and-javascript
def jsonDateTimeHandler(obj):
  """Takes an object and tries to serialize it in JSON 
  by using strftime or isoformat."""
  if hasattr(obj, "strftime"):
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
def jsonifySeminars(url, getEventList, cached,
                    cacheStillCurrent=None,
                    isJson=False):
  """Process the data obtained from url and returns an instance of CachedResult
  with the updated list of event. 

  The data is parsed with BeautifulSoup (or json.loads if isJson is true) 
  and elaborated by the function getEventList.
  
  Optionally the raw data can be compared with the cached data by means of 
  the function cacheStillCurrent. 

  The cache contains the json dump of the event list."""

  rawdata = getRawData(url, cached)

  # if we have new rawdata we proceed with the elaboration
  # otherwise (errors or current cache), we revert to the cache
  if rawdata:
    print("INFO: JSONification of ", url)
    if isJson:
      data = json.loads(rawdata)
    else:
      data = BeautifulSoup(rawdata, "html5lib")

    # we process the data only if the cache is no longer current or
    # we have no way to check if it is
    if not (cacheStillCurrent and cacheStillCurrent(data, cached)):
      event_list = getEventList(data)
      cached.update(json.dumps(list(event_list), default=jsonDateTimeHandler))

  return cached
