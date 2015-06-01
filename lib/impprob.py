# -*- encoding: utf-8 -*-
from lib.helpers import *

#########################################################
# take the data and get the events
def getSeminar(dtt_, location_, description_):

  datestring, timestring, title = list(map(lambda x: x.get_text().strip(), dtt_.findAll('td')))
  location = location_.get_text().replace('Abstract', '').strip()
  description = description_.get_text().strip()

  if 'Description' in location:
    location = 'For additional informations <a href="http://wwwf.imperial.ac.uk/~amijatov/IP/{}" target="_blank">click here</a>'.format(dtt_.a['href'])
    description += '<br/><p>{}</p>'.format(location)

  if 'All day' in timestring:
    start = parse('{0} 9:00 am'.format(datestring))
    end = parse('{0} 6:00 pm'.format(datestring))
  else:
    start = parse('{0} {1}'.format(datestring, timestring))
    end = start + relativedelta(hours=+1)

  seminar = {
    'start': start,
    'end': end,
    'title': title,
    'description': description,
    'location': location
  }

  return seminar

def getEventList(soup):
  data = soup.body.find('td', attrs={"class":"main"}).table.tbody.tr.table.tbody
  rows = data.find_all('tr')
  seminars = [getSeminar(rows[3*i],rows[3*i+1],rows[3*i+2]) 
              for i in range(len(rows)//3)]

  return seminars

#IC fortnightly seminar on topics in Mathematical Physics
def jsonifyIP(cache = CachedResult()):
  return jsonifySeminars("http://wwwf.imperial.ac.uk/~amijatov/IP/index.php", getEventList, cache)


# #########################################################
# if __name__ == "__main__":
#   print(jsonifyIP().cache)