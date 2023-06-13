from __future__ import annotations

from typing import List, Optional

import requests
from pydantic import BaseModel


class Value(BaseModel):
    id: Optional[int] = None
    code: str
    value: str


class Helper(BaseModel):
    name: str
    propertyName: str


class Filter(BaseModel):
    name: str
    type: str
    label: str
    isGlobal: bool
    values: Optional[List[Value]] = None
    visibility: List[str]
    secondaryFilters: Optional[List[str]] = None
    helpers: Optional[List[Helper]] = None


class GroupCode(BaseModel):
    name: str
    code: str
    filterName: str
    systemCodes: List[str]


class Model(BaseModel):
    filters: List[Filter]
    groupCodes: List[GroupCode]


def get_filters():
    url = 'https://api.investmoscow.ru/investmoscow/tender/v2/filtered-tenders/metadata?filterDisplay=Tender'
    res = requests.get(url)
    return Model.parse_obj(res.json())


if __name__ == '__main__':
    """
    Список фильтров которые можно использовать при отображении
    """

    filters = get_filters()
    print(filters)
