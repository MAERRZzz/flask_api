from flask import Flask
from forms import home, user, qr, errors, security, test
import locale

app = Flask(__name__, template_folder='templates')
locale.setlocale(locale.LC_ALL, '')
app.config['JSON_AS_ASCII'] = False

# TEST
app.add_url_rule('/test', view_func=test.test)

# # Главная страница
# app.add_url_rule('/', view_func=home.index)
#
# Добавления нового пользователя
app.add_url_rule('/user/add', methods=['POST'], view_func=user.add)
#
# # Сканирование QR-кода
# app.add_url_rule('/check/qr', methods=['POST'], view_func=security.auth.login_required(qr.check))
#
# # Update server
# app.add_url_rule('/git_update', methods=['POST'], view_func=ci.webhook)
#
# # Авторизация
# app.add_url_rule('/log', view_func=security.auth.login_required(security.log))

# Обрабокта ошибок
app.errorhandler(400)(errors.not_found)
app.errorhandler(404)(errors.not_found)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
