import base64
import json
from decimal import Decimal, ROUND_DOWN
from typing import Union

from pydantic import validate_arguments

from src.core.config import settings


@validate_arguments
def convert_number_to_decimal(num: Union[int, float, Decimal]) -> Decimal:
    """
    Конвертация всех числовых значений в Decimal с округлением вниз.

    На выходе получаем Decimal в формате 0.00
    """
    return Decimal(num).quantize(Decimal('0.0'), rounding=ROUND_DOWN)


def encode_data_to_base64(data: dict) -> str:
    return base64.b64encode(json.dumps(data).encode()).decode()


def decode_data_from_base64(base64_string: str) -> dict:
    return json.loads(base64.b64decode(base64_string).decode())


def get_webhook_url(endpoint: str, short_url: bool = True) -> str:
    """Генерирование разных форматов путей к webhook endpoint."""
    if short_url:
        return f"{settings.WEBHOOK_PATH}/{endpoint}"
    else:
        return f"{settings.webhook_uri}/{endpoint}"
