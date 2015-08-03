# -*- encoding: utf-8 -*-
import re
from functools import reduce
from itertools import chain

from scrapers.helpers import jsonify_seminars, tAdjust
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import requests
from bs4 import BeautifulSoup, NavigableString, Tag


#########################################################
# This part will seriously depend on the structure of the LAS page
#
# ### local helpers ###


def get_date_time_start_end(data):
    # pythrex [http://pythex.org/] could be useful for this
    regex = re.compile('(\w*,\s\d+\s\w*),\s(.*[ap]m)')
    res = regex.search(data)

    if res:
        date, times = res.groups()

        regex = re.compile('(\d+[:\.]?\d?\d?)-(\d+[:\.]?\d?\d?)([ap]m)')
        res = regex.search(times)

        if res:
            start_date_time = parse(
                date + ' 2015 ' + tAdjust(res.group(1)) + ' ' + res.group(3))
            end_date_time = parse(
                date + ' 2015 ' + tAdjust(res.group(2)) + ' ' + res.group(3))

            return start_date_time, end_date_time

    return None


def generate_description(acc, content):
    if content.name != 'strong':
        if content.name == 'em':
            acc['title'] += ' - ' + content.string.strip()
        elif content.name == 'a':
            try:
                url = content['href']
                if url[-4:] == 'html':
                    abstract_page = requests.get(url)
                    soup = BeautifulSoup(abstract_page.content.replace(
                        b"<br>", b"").replace(b"<br/>", b""))
                    abstract = next(
                        el for el in soup.body.contents
                        if type(el) == NavigableString and el.strip()[:8] == "Abstract")
                    acc['abstract'] = abstract.strip()

            # This is really bad! If I log some of the errors I will fix it
            except Exception as error:
                print("\tLAS: ", error)
                acc['abstract'] = "<a href='" + content[
                    'href'
                ] + "' target='_blank'>Click here for the abstract"
        elif type(content) != Tag:
            acc['title'] += content.strip()

    return acc


def get_seminar_info(seminar):
    return reduce(generate_description, seminar.contents[:-1],
                  {'title': '',
                   'abstract': ''})


def clean_triplets(triplet):
    start, end = get_date_time_start_end(triplet[0].string)
    location = triplet[1].strip()[:-1]

    raw_seminars = triplet[2].find_all('li')
    seminars = [get_seminar_info(seminar) for seminar in raw_seminars]

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


def admissible_triplets(triplet):
    return (type(triplet[0]) == Tag) and (triplet[0].name == "strong") and (
        type(triplet[1]) == NavigableString
    ) and (type(triplet[2]) == Tag) and (triplet[2].name == "ul")


#########################################################
# take the data and get the events
def get_event_list(soup):
    data = soup.body.contents

    triplets = filter(admissible_triplets, ((data[i], data[i + 1], data[i + 2])
                                           for i in range(len(data) - 2)))

    # We can accept empty abstracts but not empty titles
    events = filter(lambda s: s['title'] != " - ", chain.from_iterable(
        filter(lambda t: t is not None, map(clean_triplets, triplets))))

    return events


def get_las(last_update=None):
    """London Analysis and Probability Seminar"""
    return jsonify_seminars("http://www.london-analysis-seminar.org.uk/",
                            get_event_list, last_update=last_update)
