# -*- encoding: utf-8 -*-
from scrapers.helpers import jsonify_seminars
from bs4 import Tag
from dateutil.parser import parse


#########################################################
# This part will seriously depend on the structure of the LAS page


def get_seminar(data):
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


def admissible_couples(couple):
    return (type(couple[0]) == Tag) and (couple[0].name == "dt") and (
        type(couple[1]) == Tag) and (couple[1].name == "dd")


def get_event_list(soup):
    data = soup.find_all('entry')
    # We can accept empty abstracts but not empty titles
    events = filter(lambda ev: ev is not None, map(get_seminar, data))

    return events


# No longer used
# def cache_still_current(soup, last_update):
#     return timestamp(parse(soup.updated.text).replace(tzinfo=None)) > timestamp(last_update)


def get_sas(last_update=None):
    """IC Stochastic Analysis seminar"""
    return jsonify_seminars(
        "http://www3.imperial.ac.uk/imperialnewsevents/eventsfront?pid=6191_178198110_6191_178198049_178198049",
        get_event_list, last_update=last_update)


def get_taktic(last_update=None):
    """IC TAKTIC: Topology and Knot Theory at Imperial College"""
    return jsonify_seminars(
        "http://www3.imperial.ac.uk/imperialnewsevents/eventsfront?pid=5672_184390848_5672_184390833_184390833",
        get_event_list, last_update=last_update)


def get_apde(last_update=None):
    """IC Applied PDEs Seminars"""
    return jsonify_seminars(
        "http://www3.imperial.ac.uk/imperialnewsevents/eventsfront?pid=116_179821488_116_179794307_179794307",
        get_event_list, last_update=last_update)


def get_ammp(last_update=None):
    """IC Applied Mathematics and Mathematical Physics Seminar"""
    return jsonify_seminars(
        "http://www3.imperial.ac.uk/imperialnewsevents/eventsfront?pid=116_177737061_116_177736608_177736608",
        get_event_list, last_update=last_update)


def get_fd(last_update=None):
    """IC Fluid dynamics group seminar"""
    return jsonify_seminars(
        "http://www3.imperial.ac.uk/imperialnewsevents/eventsfront?pid=5732_177343692_5732_177334749_177334749",
        get_event_list, last_update=last_update)


def get_ftmp(last_update=None):
    """IC fortnightly seminar on topics in Mathematical Physics"""
    return jsonify_seminars(
        "http://www3.imperial.ac.uk/imperialnewsevents/eventsfront?pid=5751_177356114_5751_177356049_177356049",
        get_event_list, last_update=last_update)

def get_bms(last_update=None):
    """Biomathematical sciences seminar"""
    return jsonify_seminars(
        "http://www3.imperial.ac.uk/imperialnewsevents/eventsummary?s=177175253",
        get_event_list, last_update=last_update)