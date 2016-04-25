# -*- encoding: utf-8 -*-
from scrapers.helpers import jsonify_seminars
import re
import requests
from urllib.parse import quote

URLREGEX = re.compile(r"(https?://[^ ]+)")


def encode_URI(str_):
    return quote(str_, safe=' ~@#$&()*!+=:;,.?/\'')


def get_seminar(raw_seminar):
    _b = raw_seminar.begin
    if raw_seminar.has_end():
        _e = raw_seminar.end
    else:
        _e = None

    name = raw_seminar.name
    location = raw_seminar.location
    description = raw_seminar.description
    all_day = raw_seminar.all_day

    try:
        print("""
        b: {}
        e: {}
        name: {}
        location: {}
        description: {}
        all_day: {}
        """.format(
            _b, _e,
            name,
            location,
            description,
            all_day
        ))

        if location.startswith("Unknown") or location == '':
            if description != '':
                url_search = URLREGEX.search(description)
                if url_search is not None:
                    description = URLREGEX.sub(r'<a href="\1">\1</a>', description)

            if description == '':
                description += "<br /><br /><p>Be aware that dates and times shown for this event might not be reliable. \
                Please refer to the seminar official website, or any link above this paragraph, for the details.</p>"

        seminar = {
            'start': _b + " UTC",
            'end': _e + " UTC",
            'title': name,
            'description': description,
            'location': location
        }

        return seminar

    except AttributeError as e:
        print("GCAL ICS parse error: ", e)
        return None


# data is a json decoded instance
def get_event_list(cdata):

    seminars = filter(lambda ev: ev is not None, map(get_seminar, cdata.events))

    return seminars


# Google Calendar
def get_gcal(gcal_id, last_update=None):
    """Seminars from Public Google Calendar, requires gcal_id"""
    url = "https://calendar.google.com/calendar/ical/{}/public/basic.ics".format(
        gcal_id)

    if requests.head(url).status_code == requests.codes.NOT_FOUND:
        return None

    return jsonify_seminars(url,
                            get_event_list,
                            isIcs=True,
                            last_update=last_update)
