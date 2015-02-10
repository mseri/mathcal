# -*- encoding: utf-8 -*-
from lib.helpers import *

#########################################################
# This part will seriously depend on the structure of the LAS page

def getDateTimeStartEnd(data, _time):
  start = parse(data + ' 2015 ' + _time)
  end = start + relativedelta(hours=+1)
  return (start, end)

def getSeminarInfo(seminar):
  speaker = seminar('acm.nom')[0].getText().replace('\n','')
  
  if speaker != 'NO SEMINAR':
    title = seminar('i')[1].getText().strip()
    abstract = "<br/> ".join(map(lambda s: s.getText().strip(), seminar('i')[2:]))
    return (speaker + ' - ' + title, abstract + "<br/><br/><i>There will be tea in room 606 from 4:15-4:45pm</i>.")

  return (None, None)

def cleanCouple(couple):
  start, end = getDateTimeStartEnd(couple[0].string, "4:45 pm")
  location = "UCL, first floor of 25 Gordon Street, room D103"

  # TODO: Get both using regexp instead of creating this horrible warning
  if couple[1].getText().count('Title') > 1:
    start = start + relativedelta(hours=-1, minutes=-30)
    title = "WARN: two seminars"
    description = "There are probably two seminars. <a href='http://www.homepages.ucl.ac.uk/~ucahsze/seminars.html' target='_blank'>Click here for additional informations</a>."
  else:
    title, description = getSeminarInfo(couple[1].contents.pop())

  if title != None:
    seminar = {
      'start': start,
      'end': end,
      'title': title,
      'description': description,
      'location': location
    }
  else:
    seminar = None

  return seminar

def admissibleCouples(couple): 
  return (type(couple[0]) == Tag) and (couple[0].name == "dt") and  (type(couple[1]) == Tag) and (couple[1].name == "dd")

def getEventList(soup):
  data = soup.dl.contents

  couples = filter(admissibleCouples, 
    ( (data[i], data[i+1]) for i in range(len(data)-2) )
  )

  # We can accept empty abstracts but not empty titles
  events = filter(lambda ev: ev != None,
        map(cleanCouple, couples)
      )

  return events

def jsonifyNTS(cache = CachedResult()):
  return jsonifySeminars("http://www.homepages.ucl.ac.uk/~ucahsze/seminars.html", getEventList, cache)
