# -*- encoding: utf-8 -*-
from lib.helpers import jsonifySeminars, parse, relativedelta, Tag, CachedResult

#########################################################
# This part will seriously depend on the structure of the LAS page


def getSeminar(data):
  start = parse(data("imperialnewsevents:event_start_date")[0].text)
  end = parse(data("imperialnewsevents:event_end_date")[0].text)
  description = "<a href='{}' target='_blank'>Click here for additional informations</a>.".format(
      data.link["href"])
  location = ", ".join([data("imperialnewsevents:location")[0].text,
                        data("imperialnewsevents:source")[0].text,
                        data("imperialnewsevents:campus")[0].text])

  seminar = {
      'start': start,
      'end': end,
      'title': data.title.text,
      'description': description,
      'location': location
  }

  return seminar


def admissibleCouples(couple):
  return (type(couple[0]) == Tag) and (couple[0].name == "dt") and (
      type(couple[1]) == Tag) and (couple[1].name == "dd")


def getEventList(soup):
  data = soup.find_all('entry')
  # We can accept empty abstracts but not empty titles
  events = filter(lambda ev: ev != None, map(getSeminar, data))

  return events


def cacheStillCurrent(soup, cached):
  return relativedelta(parse(soup.updated.text).replace(tzinfo=None),
                       cached.last_updated).days < 0

#jsonifySAS, jsonifyTAKTIC, jsonifyAPDE, jsonifyAMMP,  jsonifyAMMP, jsonifyFD, jsonifyFTMP


#IC Stochastic Analysis seminar
def jsonifySAS(cache=CachedResult()):
  return jsonifySeminars(
      "http://www3.imperial.ac.uk/imperialnewsevents/eventsfront?pid=6191_178198110_6191_178198049_178198049",
      getEventList, cache, cacheStillCurrent)


#IC TAKTIC: Topology and Knot Theory at Imperial College
def jsonifyTAKTIC(cache=CachedResult()):
  return jsonifySeminars(
      "http://www3.imperial.ac.uk/imperialnewsevents/eventsfront?pid=5672_184390848_5672_184390833_184390833",
      getEventList, cache, cacheStillCurrent)


#IC Applied PDEs Seminars
def jsonifyAPDE(cache=CachedResult()):
  return jsonifySeminars(
      "http://www3.imperial.ac.uk/imperialnewsevents/eventsfront?pid=116_179821488_116_179794307_179794307",
      getEventList, cache, cacheStillCurrent)


#IC Applied Mathematics and Mathematical Physics Seminar
def jsonifyAMMP(cache=CachedResult()):
  return jsonifySeminars(
      "http://www3.imperial.ac.uk/imperialnewsevents/eventsfront?pid=116_177737061_116_177736608_177736608",
      getEventList, cache, cacheStillCurrent)


#IC Fluid dynamics group seminar
def jsonifyFD(cache=CachedResult()):
  return jsonifySeminars(
      "http://www3.imperial.ac.uk/imperialnewsevents/eventsfront?pid=5732_177343692_5732_177334749_177334749",
      getEventList, cache, cacheStillCurrent)


#IC fortnightly seminar on topics in Mathematical Physics
def jsonifyFTMP(cache=CachedResult()):
  return jsonifySeminars(
      "http://www3.imperial.ac.uk/imperialnewsevents/eventsfront?pid=5751_177356114_5751_177356049_177356049",
      getEventList, cache, cacheStillCurrent)

# #########################################################
# if __name__ == "__main__":
#   print(jsonifySAS().cache)
