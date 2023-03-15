from flask import request, jsonify, abort
import datetime
import base64
import time
import rsa
from databases.extension import session, Student, VisitList


# Запись присутствия студента
def check():
    # if not request.json \
    #         or not ('qr_data' in request.json) \
    #         or not ('lecture_room' in request.json):
    #     abort(400)

    # qr_data = request.json["qr_data"]
    qr_data = "106769220227267884323|QmOZijBV5JrGSyfzQvcrR/t3C79FI2Ur0EwN4ZXB6j7" \
              "RdinBF9c5uixtOptvLLibNSzo16Q4Ogn0sSp+Bsj3ez/I0F7xR+3jsBG20uCJtKh1eI" \
              "elpMS0TEvrISnR4qXf15dukMpTFX0viE6IZdy2QR8DfAxYJ28cIGoEyY89WPs="
    # lecture_room = request.json["lecture_room"]
    lecture_room = 236

    google_id = qr_data[:qr_data.find("|")]
    encrypted_time = qr_data[qr_data.find("|") + 1:]
    encrypted_time = base64.b64decode(encrypted_time)

    student = session.query(Student).filter_by(google_id=google_id).first()
    private_key = student.private_key
    private_key = rsa.PrivateKey.load_pkcs1(private_key)

    decrypted_time = rsa.decrypt(encrypted_time, private_key)
    decrypted_time = int(decrypted_time.decode())
    current_time = time.time()
    print(current_time - decrypted_time)

    if (current_time - decrypted_time) < 35:
        visit_time = current_time
        in_visit_list = session.query(VisitList).filter_by(student_id=student.id).all()
        print(type(in_visit_list))
        if in_visit_list:
            in_visit_list = in_visit_list[0] if len(in_visit_list) == 1 else in_visit_list[-1]
            if (current_time - in_visit_list.visit_time) > 30:
                add_in_list = VisitList(student.id, visit_time, lecture_room)
                session.add(add_in_list)
                session.commit()
                status = f"{student.display_name}: new visit time - {datetime.datetime.fromtimestamp(visit_time)}"
            else:
                status = f"{student.display_name} already in visit list."

        if not in_visit_list:
            add_in_list = VisitList(student.id, visit_time, lecture_room)
            session.add(add_in_list)
            session.commit()
            status = f"{student.display_name} was added in visit list."
    else:
        status = "QR-code is not actual."

    return jsonify({'status': status})
