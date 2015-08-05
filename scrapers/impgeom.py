# -*- encoding: utf-8 -*-
import re

from scrapers.helpers import jsonify_seminars
from dateutil.parser import parse


def getGASSeminar(raw_seminar):
    try:
        author, whenWhere = map(lambda em: em.get_text().strip(),
                                raw_seminar.findAll('em'))
        title = raw_seminar.strong.get_text().strip()
        abstract = raw_seminar.br.next.strip()
        day, times, location = whenWhere.split(', ')
        timereg = r"(\d+)-(\d+)([a|p]m)"
        start_, stop_, rest_ = re.match(timereg, times).groups()
    except Exception as e:
        print("GAS parsing error: ", e)
        return None

    title = "{} - {}".format(author, title)
    description = abstract
    location = "{}, Imperial College".format(location)
    start = parse("{} {}:00 {}".format(day, start_, rest_))
    end = parse("{} {}:00 {}".format(day, stop_, rest_))
    seminar = {
        'start': start,
        'end': end,
        'title': title,
        'description': description,
        'location': location
    }

    return seminar


def getLTGSeminar(raw_seminar):
    if "Abstract:" in raw_seminar.get_text().strip():
        return None

    try:
        author = raw_seminar.em.get_text().strip().replace(".", "")
        title = raw_seminar.strong.get_text().strip()
        whenWhere = raw_seminar.strong.next.next.strip()
        abstract = "<a href='http://geometry.ma.ic.ac.uk/seminar/' target='_blank'>Click here</a> for more informations."
        day, times, location = whenWhere.split(', ')
        timereg = r"(\d+\.?\d*)-(\d+\.?\d*)([a|p]m)"
        start_, stop_, rest_ = re.match(timereg, times).groups()
        start_ = start_.replace(".",
                                ":") if "." in start_ else "{}:00".format(start_)
        stop_ = stop_.replace(".", ":") if "." in stop_ else "{}:00".format(stop_)
    except Exception as e:
        print("GAS parsing error: ", e)
        return None

    title = "{} - {}".format(author, title)
    description = abstract
    location = "{}, Imperial College".format(location[:-1])
    start = parse("{} {} {}".format(day, start_, rest_))
    end = parse("{} {} {}".format(day, stop_, rest_))
    seminar = {
        'start': start,
        'end': end,
        'title': title,
        'description': description,
        'location': location
    }

    return seminar


def getEventListGAS(soup):
    raw_seminars = soup.findAll("div",
                                attrs={"class": "postentry"})[0].findAll("p")
    seminars = filter(lambda s: s is not None, map(getGASSeminar, raw_seminars))
    return seminars


def getEventListLTGS(soup):
    raw_seminars = soup.findAll("div",
                                attrs={"class": "postentry"})[0].findAll("p")
    seminars = filter(lambda s: s is not None, map(getLTGSeminar, raw_seminars))
    return seminars


def get_ipgas(last_update=None):
    """IC Geometry and Analysis Seminar"""

    return jsonify_seminars("http://geometry.ma.ic.ac.uk/gaseminar/",
                        getEventListGAS, last_update=last_update)


def get_ipltgs(last_update=None):
    """IC The London Topology and Geometry Seminar"""
    return jsonify_seminars("http://geometry.ma.ic.ac.uk/seminar/",
                           getEventListLTGS, last_update=last_update)
