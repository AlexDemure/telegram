
def prepare_response_get_verify_code(verify_code: str) -> str:
    return f"<i>Процесс получения кода подтверждения.</i>\n" \
           f"Для получения кода необходимо перейти по ссылке, после перехода по ссылке произойдет редирект.\n" \
           f"<u>get параметр ?code=******* необходимо скопировать и вставить</u>.\n " \
           f"<a href='{verify_code}'>Ссылка с кодом.</a>"