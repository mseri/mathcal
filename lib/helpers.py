# -*- encoding: utf-8 -*-

import os
import requests
import re

from bs4 import BeautifulSoup, NavigableString, Tag

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from datetime import date, datetime

from functools import reduce
from itertools import chain

import json

#########################################################
# Dealing with the request is generic. We will reuse this part later on
def getFilePath(fileName):
    return os.path.join(os.path.dirname(__file__), fileName)

def saveReqToFile(req, fileName, cached):
  # Save to file the content of request...
  theFile = getFilePath(fileName)

  remoteLastModified = (parse(req.headers['last-modified']).replace(tzinfo=None) - datetime(1970,1,1).replace(tzinfo=None)).total_seconds()

  if cached.lastUpdate > remoteLastModified and cached.cache != "":
    print ("Cache still current, skipping download of %s" % (fileName))
    return False

  print("Saving %s to %s" % (req.url, fileName))
  with open(theFile, 'wb') as f:
    # Is possible to do f.write(theFile.content)
    # However, this is the recommend way for (possible) large responses
    # Write in chunks... I decide in 512.
    # http://stackoverflow.com/questions/13137817/how-to-download-image-using-requests
    for chunk in req.iter_content(512):
      f.write(chunk)

  return True

def getRequest(url):
  return requests.get(url, stream=True)

def makeSoup(fileName):
  with open(getFilePath(fileName), 'r') as f:
      soup = BeautifulSoup(f,"html5lib")

  return soup

#########################################################
# if the time has only one/two digit adds 'zero minutes'
# otherwise it simply replace the "." separating hours and minutes
# with the ":"
def tAdjust(sTime):
  if len(sTime) <= 2:
    return sTime + ":00"

  return sTime.replace('.', ':')

#########################################################
class CachedResult():
  def __init__(self):
    self.cache = ""
    self.lastUpdate = self.epochDate(datetime(1970,1,1))

  def update(self, cache):
    self.cache = cache
    self.lastUpdate  = self.epochDate(datetime.now())

  def epochDate(self, date):
    return (date.replace(tzinfo=None) - datetime(1970,1,1).replace(tzinfo=None)).total_seconds()

#########################################################
# http://stackoverflow.com/questions/455580/json-datetime-between-python-and-javascript
def jsonDateTimeHandler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    # elif isinstance(obj, ...):
    #     return ...
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))

#########################################################
# generate JSONFrom the list of dictionaries
def jsonifySeminars(url, _tag, getEventList, cached):
  tag = _tag.lower()
  fileName = tag + '.html'

  if saveReqToFile(getRequest(url), fileName, cached):
    print("JSONification of " + tag)
    soup = makeSoup(fileName)
    eventList = getEventList(soup)
    cached.update(json.dumps(list(eventList), default=jsonDateTimeHandler))

  return cached