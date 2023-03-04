from flask import make_response, jsonify


# Обработка ошибок
def not_found(error):
    return make_response(jsonify(error=str(error)))
