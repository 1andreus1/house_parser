from enum import Enum

import requests


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


class HTTPMethod(Enum):
    GET = requests.get
    POST = requests.post


class DecodeTo(Enum):
    TEXT: object = lambda res: res.text
    JSON: object = lambda res: res.json()


def get_url(method, decoder, url, **kwargs):
    res = method(url, **kwargs)
    res.encoding = ENCODING
    return decoder(res)


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
