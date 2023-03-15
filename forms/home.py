from flask import render_template, request
import datetime
from databases import extension


def index():
    data = list()
    sorting = dict()
    lessons_time = ['8:00', '9:40', '11:30', '13:10', '14:50', '16:30', '18:10']
    check_in_time = extension.execute_read_query(
        'Select *, check_in_time as "check_in_time2[timestamp]" from lesson_list where user_id = "9" ')
    print()
    if request.args.get('date') and request.args.get('time') and request.args.get('lecture_room'):
        date = request.args.get('date')
        time = request.args.get('time')
        lecture_room = request.args.get('lecture_room')
        end_time = lessons_time[time_index + 1] \
            if (time_index := (lessons_time.index(time))) < len(lessons_time) - 1 else '19:40'
        print(end_time)

        date_form = datetime.datetime.strptime(date, "%Y-%m-%d")
        date_dict = datetime.datetime.strftime(date_form, '%B, %d').replace('0', ' ')
        sorting = {'date_form': request.args.get('date'),
                   'date': date_dict,
                   'time': request.args.get('time'),
                   'lecture_room': request.args.get('lecture_room')}

        data_2 = f'''Select *, group_concat(STRFTIME("%H:%M", check_in_time), " - ") as check_time from lesson_list, user 
                    where check_in_time between "{date + ' ' + time}" and "{date + ' ' + end_time}" 
                    and lecture_room = {lecture_room} and user_id=user.id'''
        data_2 = extension.execute_read_query(data_2)
        data = data_2 if data_2[0]['id'] else list()
        print(data)
    return render_template('index.html', lessons=lessons_time, data=data, sorting=sorting)
