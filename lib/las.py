# -*- encoding: utf-8 -*-
from lib.helpers import *

#########################################################
# This part will seriously depend on the structure of the LAS page
#
# ### local helpers ###

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
          soup = BeautifulSoup(abstractPage.content.replace(b"<br>",b"").replace(b"<br/>",b""))
          abstract = next(el for el in soup.body.contents if  type(el) == NavigableString and el.strip()[:8] == "Abstract")
          acc['abstract'] = abstract.strip()
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
    # print('\tSeminars processed')
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

  # print('\tNot enough data to process')
  return None

def admissibleTriplets(triplet): 
  return (type(triplet[0]) == Tag) and (triplet[0].name == "strong") and (type(triplet[1]) == NavigableString) and (type(triplet[2]) == Tag) and (triplet[2].name == "ul")

#########################################################
# take the data and get the events
def getEventList(soup):
  data = soup.body.contents

  triplets = filter(admissibleTriplets, 
    ( (data[i], data[i+1], data[i+2]) for i in range(len(data)-2) )
  )

  # We can accept empty abstracts but not empty titles
  events = filter(lambda s: s['title'] != " - ",
    chain.from_iterable(
      filter(lambda t: t != None,
        map(cleanTriplets, triplets)
      )))

  return events

def jsonifyLAS(cache = CachedResult()):
  return jsonifySeminars("http://www.london-analysis-seminar.org.uk/", "LAS", getEventList, cache)

#########################################################
if __name__ == "__main__":
  print(jsonifyLAS().cache)
