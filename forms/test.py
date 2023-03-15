from flask import jsonify
import datetime
import time

from databases.extension import session, Event, Class, Student


def test():
    qr_time = int(time.time())
    qr_weekday = time.strftime('%A', time.localtime(qr_time))[:2].upper()
    today = datetime.date.today()

    pattern_date, pattern_timestamp = '%Y-%m-%d', '%Y-%m-%d %H:%M:%S'

    time_list = {
        '08:00': '09:30',
        '09:40': '11:10',
        '11:30': '13:00',
        '13:10': '14:40',
        '14:50': '16:20',
        '16:30': '18:00'}

    lesson_start_time = ''

    for start, end in time_list.items():
        start_timestamp = int(
            time.mktime(time.strptime(f"{today.strftime(pattern_date)} {start}:00", pattern_timestamp)))
        end_timestamp = int(
            time.mktime(time.strptime(f"{today.strftime(pattern_date)} {end}:00", pattern_timestamp)))
        if start_timestamp < qr_time < end_timestamp:
            lesson_start_time = start

    query = session.query(Event, Class).filter(Event.summaryId == Class.id, Event.location.contains('236'),
                                               Event.start.contains(lesson_start_time),
                                               Event.recurrence[1].like(f'%BYDAY={qr_weekday}%')).all()
    for i in query:
        print(i[0].recurrence)
    test_event = [f'{i[0].location.replace(", КИПУ", "")} {i[1].name} {i[0].start}' for i in query]

    return jsonify(test_event)
