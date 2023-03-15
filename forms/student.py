from flask import request, abort, jsonify
from databases.extension import session, Student
import rsa


# Добавление пользователей в БД
def add():
    if not (json := request.json) \
            or 'email' not in json \
            or 'display_name' not in json \
            or 'google_id' not in json \
            or 'photo_url' not in json:
        abort(400)

    email = json['email']
    display_name = json['display_name']
    google_id = json['google_id']
    photo_url = json['photo_url']

    student = session.query(Student).filter_by(email=email).first()

    if not student:
        # Отделить имя и фамилию в атрибуты для сортировки
        # first_name = display_name.split()[0]
        # last_name = display_name.split()[-1]

        public_key, private_key = rsa.newkeys(1024)
        public_key = public_key.save_pkcs1().decode('utf-8')
        private_key = private_key.save_pkcs1().decode('utf-8')

        student = Student(email, display_name, google_id, public_key, private_key)
        session.add(student)
        session.commit()

    return jsonify({'email': student.email,
                    'display_name': student.display_name,
                    'google_id': student.google_id,
                    'public_key': student.public_key,
                    'photo_url': photo_url})
