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

def saveReqToFile(req, fileName):
  # Save to file the content of request...
  theFile = getFilePath(fileName)

  lastModified = (parse(req.headers['last-modified']).replace(tzinfo=None) - datetime(1970,1,1).replace(tzinfo=None)).total_seconds()

  if os.path.isfile(fileName) and os.path.getmtime(fileName).replace(tzinfo=None) > lastModified:
    printTab("File %s already present, skipping download" % (fileName))
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
      soup = BeautifulSoup((f))

  return soup

#########################################################
# This part will seriously depend on the structure of the LAS page

# if the time has only one/two digit adds 'zero minutes'
# otherwise it simply replace the "." separating hours and minutes
# with the ":"
def tAdjust(sTime):
  if len(sTime) <= 2:
    return sTime + ":00"

  return sTime.replace('.', ':')

def getDateTimeStartEnd(data):
  # pythrex [http://pythex.org/] could be useful for this
  regex = re.compile('(\w*,\s\d+\s\w*),\s(.*[ap]m)')
  res = regex.search(data)

  if res:
    date, times = res.groups()

    regex = re.compile('(\d+[:\.]?\d?\d?)-(\d+[:\.]?\d?\d?)([ap]m)')
    res = regex.search(times)

    if res:
      startDateTime = parse(date + ' 2015 ' +  tAdjust(res.group(1)) + ' ' + res.group(3))
      endDateTime = parse(date + ' 2015 ' + tAdjust(res.group(2)) + ' ' + res.group(3))

      return (startDateTime, endDateTime)
  
  return None

def generateDescription(acc, content):
  if content.name != 'strong':
    if content.name == 'em':
      acc['title'] += ' - ' + content.string.strip()
    elif content.name == 'a':
      try:
        url = content['href']
        if url[-4:] == 'html':
          abstractPage = requests.get(url)
          soup = BeautifulSoup(abstractPage.content)
          abstract = next(el for el in soup.body.contents if  type(el) == NavigableString and el.strip()[:8] == "Abstract")
          acc['abstract'] += abstract.strip()
      except:
        acc['abstract'] = "<a href='" + content['href'] + "' target='_blank'>Click here for the abstract"
    elif type(content) != Tag:
      acc['title'] += content.strip()

  return acc

def getSeminarInfo(seminar):
  return reduce(generateDescription, seminar.contents[:-1], {'title':'', 'abstract':''})

def cleanTriplets(triplet):
  start, end = getDateTimeStartEnd(triplet[0].string)
  location = triplet[1].strip()[:-1]

  rawSeminars = triplet[2].find_all('li')
  seminars = list(map(getSeminarInfo, rawSeminars))

  if start and end and location and seminars and len(seminars) == 2:
    seminar1 = {
      'start': start,
      'end': start + relativedelta(hours=+1),
      'title': seminars[0]['title'],
      'description': seminars[0]['abstract'],
      'location': location
    }

    seminar2 = {
      'start': end + relativedelta(hours=-1),
      'end': end,
      'title': seminars[1]['title'],
      'description': seminars[1]['abstract'],
      'location': location
    }
    return [seminar1, seminar2]

  return None

def admissibleTriplets(triplet):
  return (type(triplet[0]) == Tag) and (triplet[0].name == "strong") and (type(triplet[1]) == NavigableString) and (type(triplet[2]) == Tag) and (triplet[2].name == "ul")

def getEventList(soup):
  data = soup.body.contents

  triplets = filter(admissibleTriplets, 
    ( (data[i], data[i+1], data[i+2]) for i in range(len(data)-2) )
  )

  # The final weird sum is to concatenate the lists
  events = filter(lambda s: s['title'] != " - " and s['description'] != "",
    chain.from_iterable(
      filter(lambda t: t != None,
        map(cleanTriplets, triplets)
      )))

  return events


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
def jsonifyLAS(cachedLAS = None):
  if cachedLAS == None:
    cachedLAS = ""

  LAS = 'las.html'
  if saveReqToFile(getRequest("http://www.london-analysis-seminar.org.uk/"), LAS) or cachedLAS == "":
    print("JSONification of London Analysis Seminar")
    soup = makeSoup(LAS)
    eventList = getEventList(soup)

    cachedLAS = json.dumps(list(eventList), default=jsonDateTimeHandler)

  return cachedLAS

if __name__ == "__main__":
  print(jsonifyLAS())
