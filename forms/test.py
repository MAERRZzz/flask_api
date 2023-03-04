from flask import jsonify
from pprint import pprint

from databases.extension import session, User, Event, Class


def test():
    query = session.query(Event, Class).filter(Event.summaryId == Class.id).filter(Event.location.contains('236')).all()
    test_event = list(f'{i[0].location.replace(", КИПУ", "")} {i[1].name} {i[0].start}' for i in query)
    pprint(test_event)

    return jsonify(test_event)
