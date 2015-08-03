# -*- encoding: utf-8 -*-
from scrapers.helpers import jsonify_seminars
from dateutil.parser import parse
import re
import requests
from urllib.parse import quote

WWREGEX = re.compile(
    r"When: (\w{3} \w{3} \d+, \d{4} \d+:?\d*[ap]m) to ([^§]*\d+:?\d*[ap]m).*Where: ([^§]*)§+.*")
DESCREGEX = re.compile(r".*Event Description: (.*)")


def encode_URI(str_):
    return quote(str_, safe=' ~@#$&()*!+=:;,.?/\'')


def get_seminar(raw_seminar):
    title_obj = raw_seminar['title']
    title = title_obj[
        '$t'
    ] if 'html' in title_obj['type'] else encode_URI(title_obj['$t'])

    # Workaround for duplicate London Analysis Seminar from Imperial Analysis calendar
    if "LANS" in title or "London Analysis and Probability Seminar" in title:
        return None

    content_obj = raw_seminar['content']
    content_ = content_obj[
        '$t'
    ] if 'html' in content_obj['type'] else encode_URI(content_obj['$t'])

    # Get When and Where from the formatted content in the google calendar string
    # Takes a string of the form
    #
    #   When: Thu Feb 19, 2015 3pm to 4pm \nGMT\u003cbr /\u003e\n\n\u003cbr /\u003eWhere: room S423\n\u003cbr /\u003eEvent Status: confirmed\n\u003cbr /\u003eEvent Description: some description
    #
    # strips it and then scrapes from it date, time, location and description.
    content = re.sub(r"(<br \/>|\n)", "§", content_)
    ww_match = WWREGEX.match(content)

    if ww_match is None or len(ww_match.groups()) < 3:
        return None
    else:
        ww_data = ww_match.groups()

    # Fix start and stop datetime format:
    # get (\d\d?)([ap]m) and make into $1:00 $2
    start_ = re.sub(r"([ap]m)", r" \1", ww_data[0])
    start_ = re.sub(r" (\d\d?) ", r" \1:00 ", start_)

    # Add the day in front of the stop time string
    # and fix the time
    stop_ = re.sub(r"\d\d?:?\d?\d?\s?[ap]m", ww_data[1], ww_data[0])
    stop_ = re.sub(r"([ap]m)", r" \1", stop_)
    stop_ = re.sub(r" (\d\d?) ", r" \1:00 ", stop_)

    location = ww_data[2]

    desc_match = DESCREGEX.match(content)

    if desc_match:
        description = re.sub(r"§", '<br />', desc_match.groups()[0])
    else:
        description = ''

    start = parse(start_)
    end = parse(stop_)

    seminar = {
        'start': start,
        'end': end,
        'title': title,
        'description': description,
        'location': location
    }

    return seminar


# data is a json decoded instance
def get_event_list(jdata):
    data = jdata['feed']['entry']
    seminars = filter(lambda ev: ev is not None, map(get_seminar, data))

    return seminars


# Google Calendar
def get_gcal(gcal_id, last_update=None):
    """Seminars from Public Google Calendar, requires gcal_id"""
    url = "https://www.google.com/calendar/feeds/{}/public/basic?alt=json&hl=en".format(
        gcal_id)

    if requests.head(url).status_code == requests.codes.NOT_FOUND:
        return None

    return jsonify_seminars(url, get_event_list, isJson=True, last_update=last_update)
