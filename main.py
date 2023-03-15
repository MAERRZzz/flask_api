from flask import Flask
from forms import home, student, qr, errors, security, test
import locale

app = Flask(__name__, template_folder='templates')
# locale.setlocale(locale.LC_ALL, '')
app.config['JSON_AS_ASCII'] = False

# TEST
app.add_url_rule('/test', view_func=test.test)

# Главная страница
# app.add_url_rule('/', view_func=home.index)

# Добавления нового пользователя
app.add_url_rule('/student/add', methods=['POST'], view_func=student.add)

# Сканирование QR-кода
# app.add_url_rule('/check/qr', methods=['POST'], view_func=security.auth.login_required(qr.check))
app.add_url_rule('/check/qr', view_func=qr.check)

# Update server
# app.add_url_rule('/git_update', methods=['POST'], view_func=ci.webhook)

# Авторизация
# app.add_url_rule('/log', view_func=security.auth.login_required(security.log))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
