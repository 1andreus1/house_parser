import time
from enum import Enum
from typing import Any

import requests

from exceptions import TooManyRequestsError

ENCODING = 'utf-8'
EXCEPTION_WORDS = (
    'москва',
    'российская федерация',
    'округ',
    'этаж',
    'квартира',
    'кв.',
    'ком.',
    'пом',
    'помещение'
)
CONVERSION_FACTORS = {
    'км': 1000,
    'м': 1,
    'см': 0.01,
}

SINGLE_FIELDS = (
    'orderBy',
    'orderAsc',
    'tenderStatus',
    'pageNumber',
    'pageSize'
)

ERRORS_FOR_RETRY = (
    TooManyRequestsError,
    ConnectionError,
)
MAX_RETRIES = 6


def wait_for_response(func) -> Any:
    def wrapper(*args, **kwargs) -> Any:
        delay = 1

        for _ in range(MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except ERRORS_FOR_RETRY:
                time.sleep(delay)
                delay *= 2

        return func(*args, **kwargs)

    return wrapper


class HTTPMethod(Enum):
    GET = requests.get
    POST = requests.post


class DecodeTo(Enum):
    TEXT: object = lambda res: res.text
    JSON: object = lambda res: res.json()


@wait_for_response
def get_url(method, decoder, url, **kwargs):
    res = method(url, **kwargs)
    res.encoding = ENCODING
    check_status_code(res.status_code)
    return decoder(res)


def check_status_code(status_code: int) -> None:
    if status_code == 503:
        raise TooManyRequestsError


def clean_address(address):
    address_parts = address.split(',')
    clean_parts = [
        part.strip() for part in address_parts if
        not any(word.lower() in part.lower()
                for word in EXCEPTION_WORDS)
    ]

    clean_address = ', '.join(clean_parts)
    return clean_address


def convert_to_meters(s: str) -> float:
    try:
        s = s.strip().lower().replace('.', '')
        value, unit = s.split()
        return float(value) * CONVERSION_FACTORS[unit]
    except (Exception,):
        return None
