# -*- encoding: utf-8 -*-

from bs4 import Tag
from datetime import datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from scrapers.helpers import jsonify_seminars


#########################################################
# This part will seriously depend on the structure of the LAS page


def get_date_time_start_end(data, _time):
    year = " {} ".format(datetime.now().year)
    start = parse(data + year + _time)
    end = start + relativedelta(hours=+1)
    return start, end


def get_seminar_info(seminar):
    try:
        speaker = seminar('b')[0].getText().strip()

        if speaker != 'NO SEMINAR':
            title = seminar('i')[1].getText().strip()
            abstract = "<br/> ".join(map(lambda s: s.getText().strip(),
                                         seminar('i')[2:]))
            return (speaker + ' - ' + title, abstract +
                    "<br/><br/><i>There will be tea in room 606 from 4:15-4:45pm</i>.")
    except (IndexError, TypeError, AttributeError):
        # log the error
        pass
    return None, None


def clean_couple(couple):
    start, end = get_date_time_start_end(couple[0].string, "4:45 pm")
    location = "UCL, first floor of 25 Gordon Street, room D103"

    # TODO: Get both using regexp instead of creating this horrible warning
    if couple[1].getText().count('Title') > 1:
        start = start + relativedelta(hours=-1, minutes=-30)
        title = "WARN: two seminars"
        description = "There are probably two seminars. <a href='http://www.homepages.ucl.ac.uk/~ucahsze/seminars.html' target='_blank'>Click here for additional informations</a>."
    else:
        title, description = get_seminar_info(couple[1])

    if title is not None:
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


def admissible_couples(couple):
    return (type(couple[0]) == Tag) and (couple[0].name == "dt") and (
        type(couple[1]) == Tag) and (couple[1].name == "dd")


def get_event_list(soup):
    data = soup.dl.contents

    couples = filter(admissible_couples, ((data[i], data[i + 1])
                                          for i in range(len(data) - 2)))

    # We can accept empty abstracts but not empty titles
    events = filter(lambda ev: ev is not None, map(clean_couple, couples))

    return events


def get_nts(last_update=None):
    """Number Theory Seminar"""
    return jsonify_seminars(
        "http://www.homepages.ucl.ac.uk/~ucahsze/seminars.html", get_event_list,
        last_update=last_update)
