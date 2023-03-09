from flask import request, abort, jsonify
from databases.extension import session, User
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

    user = session.query(User).filter_by(email=email).first()

    if not user:
        # Отделить имя и фамилию в атрибуты для сортировки
        # first_name = display_name.split()[0]
        # last_name = display_name.split()[-1]

        public_key, private_key = rsa.newkeys(1024)
        public_key = public_key.save_pkcs1().decode('utf-8')
        private_key = private_key.save_pkcs1().decode('utf-8')

        user = User(email, display_name, google_id, public_key, private_key)
        session.add(user)
        session.commit()

    return jsonify({'email': user.email,
                    'display_name': user.display_name,
                    'google_id': user.google_id,
                    'public_key': user.public_key,
                    'photo_url': photo_url})
