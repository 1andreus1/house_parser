from __future__ import annotations

from typing import List, Optional
from urllib.parse import parse_qs, urlparse

from pydantic import BaseModel

from models.models import BaseModelConfig
from utils.utils import SINGLE_FIELDS


class Range(BaseModel):
    min: str
    max: str


class BaseFilterParams(BaseModelConfig):
    """"
    Эти поля нельзя трогать
    """
    page_number: int = 1
    page_size: int = 1


class FilterParams(BaseFilterParams):
    order_by: Optional[str]  # Поле для сортировки результатов
    order_asc: Optional[bool]  # Сортировка по возрастанию (True) или убыванию (False)

    object_types: Optional[List[str]]  # Типы объектов
    object_kinds: Optional[List[str]]  # Виды торгов

    price: Optional[Range]  # Диапазон начальной цены, руб
    location: Optional[Range]  # Диапазон расположения
    count_rooms: Optional[List[str]]  # Количество комнат в квартире
    entrance_types: Optional[List[str]]  # Типы входов в нежилое помещение
    functionality_purposes: Optional[List[str]]  # Функциональное назначение объектов
    object_forms: Optional[List[str]]  # Формы торгов
    realization_programs: Optional[List[str]]  # Программы реализации
    tender_status: Optional[str]  # Состояние торгов

    area: Optional[Range]  # Диапазон площади, м²
    area_apartment: Optional[Range]  # Диапазон площади квартиры, м²
    area_car_place: Optional[Range]  # Диапазон площади машино-места, м²
    area_no_living: Optional[Range]  # Диапазон площади нежилого помещения, м²
    area_ground: Optional[Range]  # Диапазон площади земельного участка, м²
    area_no_stationary: Optional[Range]  # Диапазон площади нестационарного объекта, м²
    area_building: Optional[Range]  # Диапазон площади здания, м²
    area_on_land_building: Optional[Range]  # Диапазон площади здания на земельном участке, м²
    area_room: Optional[Range]  # Диапазон площади комнат, м²
    area_construction: Optional[Range]  # Диапазон площади сооружения, м²
    area_no_capital: Optional[Range]  # Диапазон площади некапитального объекта, м²
    area_in_progress_construction: Optional[Range]  # Диапазон площади объекта незавершенного строительства, м²
    area_share_in_apartment: Optional[Range]  # Диапазон площади доли в квартире, м²

    no_living_room_floors: Optional[List[str]]  # Этажи для нежилых помещений
    number_floors: Optional[Range]  # Диапазон этажности, этажей
    floor: Optional[Range]  # Диапазон этажей
    floor_apartment: Optional[Range]  # Диапазон этажей для квартиры
    floor_car_place_room: Optional[Range]  # Диапазон этажей для машино-места
    floor_room: Optional[Range]  # Диапазон этажей для комнаты
    floor_share_apartment_room: Optional[Range]  # Диапазон этажей для доли в квартире

    number_floors_apartment: Optional[Range]  # Диапазон этажности для квартиры
    number_floors_no_living: Optional[Range]  # Диапазон этажности для нежилого помещения
    number_floors_building: Optional[Range]  # Диапазон этажности для здания
    number_floors_room: Optional[Range]  # Диапазон этажности для комнаты
    number_floors_share_in_apartment: Optional[Range]  # Диапазон этажности для доли в квартире

    subway_stations: Optional[List[str]]  # Список станций метро
    districts: Optional[List[str]]  # Список районов
    transport_categories: Optional[List[str]]  # Категории транспортных средств


def parse_url(url):
    parsed_url = urlparse(url)
    query_dict = parse_qs(parsed_url.query)

    res_converted = {}
    for key, value in query_dict.items():
        if query_dict[key][0] == 'true':
            res_converted[key] = True

        elif query_dict[key][0] == 'false':
            query_dict[key] = False
            res_converted[key] = query_dict[key][0]

        elif key in SINGLE_FIELDS:
            res_converted[key] = value[0]

        elif key.endswith(".min") or key.endswith(".max"):
            range_key = key[:-4]
            if range_key not in res_converted:
                res_converted[range_key] = {}
            res_converted[range_key][key[-3:]] = value[0]

        elif key.startswith("price") or \
                key.startswith("area") or \
                key.startswith("floor") or \
                key.startswith(
                    "number_floors"):

            res_converted[key] = Range(
                min=value[0],
                max=value[1]
            )

        else:
            res_converted[key] = value

    filter_params = FilterParams.parse_obj(res_converted)
    return filter_params
