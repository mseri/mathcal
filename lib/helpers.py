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

from tempfile import gettempdir
from zlib import crc32

import json

#########################################################
# Dealing with the request is generic. We will reuse this part later on
def getFilePath(fileName):
    return os.path.join(gettempdir(), fileName)

def saveReqToFile(req, fileName, cached):
  # Save to file the content of request...
  theFile = getFilePath(fileName)

  try: 
    remoteLastModified = epochDate(parse(req.headers['last-modified']))
  except:
    remoteLastModified = None

  if remoteLastModified and cached.lastUpdate > remoteLastModified and cached.cache != "":
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

def epochDate(date):
  return (date.replace(tzinfo=None) - datetime(1970,1,1).replace(tzinfo=None)).total_seconds()

class CachedResult():
  def __init__(self):
    self.cache = ""
    self.lastUpdate = epochDate(datetime(1970,1,1))

  def update(self, cache):
    self.cache = cache
    self.lastUpdate  = epochDate(datetime.now())

#########################################################
# http://stackoverflow.com/questions/455580/json-datetime-between-python-and-javascript
def jsonDateTimeHandler(obj):
    if hasattr(obj, "strftime"):
        return obj.strftime("%a %b %d, %Y %I:%M %p")
    # if hasattr(obj, 'isoformat'):
    #     return obj.isoformat()
    # elif isinstance(obj, ...):
    #     return ...
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))

#########################################################
# generate JSONFrom the list of dictionaries
def jsonifySeminars(url, getEventList, cached, cacheStillCurrent=None):
  tag = str(crc32(url.encode("utf-8")))
  fileName = tag + '.html'

  if saveReqToFile(getRequest(url), fileName, cached):
    print("JSONification of " + tag)
    soup = makeSoup(fileName)

    if cacheStillCurrent and cacheStillCurrent(soup, cached):
      return cached
      
    eventList = getEventList(soup)
    cached.update(json.dumps(list(eventList), default=jsonDateTimeHandler))

  return cached