server_response_codes = {
    # информационные сообщения:
    '100': "базовое уведомление",
    '101': "важное уведомление",
    # 2xx — успешное завершение:
    '200': "OK",
    '201': "created",
    '202': "accepted",
    # 4xx — ошибка на стороне клиента:
    '400': "неправильный запрос/JSON-объект",
    '401': "не авторизован",
    '402': "неправильный логин/пароль",
    '403': "forbidden",
    '404': "not found — пользователь/чат отсутствует на сервере",
    '409': "conflict — уже имеется подключение с указанным логином",
    '410': "gone — адресат существует, но недоступен (offline)",
    # 5xx — ошибка на стороне сервера:
    '500': "ошибка сервера"
}

