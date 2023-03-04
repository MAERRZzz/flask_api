from flask import request, jsonify, abort
import datetime
import base64
import time
import rsa
from databases import extension


# Запись присутствия студента
def check():
    if not request.json or not ('qr_data' in request.json) or not ('lecture_room' in request.json):
        abort(400)

    qr_data = request.json["qr_data"]
    lecture_room = request.json["lecture_room"]

    google_id = qr_data[:qr_data.find("|")]
    encrypted_time = qr_data[qr_data.find("|") + 1:]
    print(f"{google_id}\n{encrypted_time}\n")
    encrypted_time = base64.b64decode(encrypted_time)

    user = f'''Select * from user where google_id="{google_id}"'''
    user = extension.execute_read_query(user)[0]
    private_key = user["private_key"]
    private_key = rsa.PrivateKey.load_pkcs1(private_key)

    decrypted_time = rsa.decrypt(encrypted_time, private_key)
    decrypted_time = int(decrypted_time.decode())

    current_time = time.time()

    print(current_time - decrypted_time)
    if (current_time - decrypted_time) < 35:
        current_date = datetime.datetime.now()
        in_lesson_list = f'''Select *, check_in_time as "timestamp[timestamp]" from lesson_list
                                where user_id = "{user['id']}" '''
        in_lesson_list = extension.execute_read_query(in_lesson_list)
        if in_lesson_list:
            in_lesson_list = in_lesson_list[0] if len(in_lesson_list) == 1 else in_lesson_list[-1]
        print(in_lesson_list)

        if not in_lesson_list:

            add_in_list = f'''INSERT INTO lesson_list (user_id, check_in_time, lecture_room) 
                            VALUES ("{user['id']}", "{current_date}", "{lecture_room}");'''
            extension.execute_query(add_in_list)
            status = 'Added'
        elif in_lesson_list and ((current_time - (in_lesson_list['timestamp'].timestamp())) > 30):
            add_in_list = f'''INSERT INTO lesson_list (user_id, check_in_time, lecture_room) 
                                        VALUES ("{user['id']}", "{current_date}", "{lecture_room}");'''
            extension.execute_query(add_in_list)
            status = f"New check-in time - {current_date}"
        else:
            status = f"{user['displayName']} already in list."
    else:
        status = "QR-code is not actual."

    return jsonify({'status': status})
