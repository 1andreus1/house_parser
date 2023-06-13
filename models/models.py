from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, List

from camelsnake import snake_to_camel
from pydantic import BaseModel, validator

from utils.utils import clean_address


class BaseModelConfig(BaseModel):
    class Config:
        alias_generator = snake_to_camel
        allow_population_by_field_name = True


class Images(BaseModelConfig):
    url: Optional[str]


class InvestInfo(BaseModelConfig):
    id: int  # Уникальный идентификатор элемента.
    url: str  # URL элемента.
    object_type_name: Optional[str]  # Название типа объекта.
    object_area: Optional[float]  # Площадь элемента.
    is_io_area_in_hectars: Optional[bool]  # Флаг, указывающий, является ли площадь элемента в гектарах.
    address: str  # Адрес элемента.
    start_price: Optional[int]  # Начальная цена элемента.
    price_per_square: Optional[int]  # Цена за квадратный метр элемента.
    floors: Optional[int]  # Количество этажей.
    room_floors: Optional[int]  # Этаж.
    rooms_count: Optional[int]  # Количество комнат.
    request_end_date: Optional[datetime]  # Дата окончания запроса.
    tender_date: Optional[datetime]  # Дата тендера.

    attached_pics: Optional[List[Images]]
    image_url: Optional[str]
    deposit: Optional[int]  # Размер задатка.
    clean_address: Optional[str]  # Очищенный адрес элемента.

    @validator('tender_date', 'request_end_date')
    def add_three_hours(cls, value):
        if isinstance(value, datetime):
            value += timedelta(hours=3)
            return value
        return None

    @validator('room_floors', pre=True)
    def return_first_element(cls, value):
        if value is None:
            return None
        if isinstance(value, list) and len(value) > 0:
            return value[0]
        return 1

    @validator('object_area', pre=True, always=True)
    def convert_to_square_meters(cls, v, values):
        if values.get('is_io_area_in_hectars') and v:
            return v * 10000
        return v

    @validator('clean_address', always=True)
    def set_clean_address(cls, v, values):
        return clean_address(values['address'])

    @validator('image_url', always=True)
    def get_first_url(cls, v, values):
        if values.get('attached_pics'):
            return values['attached_pics'][0].url
        else:
            return None


class FlatInfo(BaseModel):
    city: Optional[str]
    district: Optional[str]
    region: Optional[str]
    building_year: Optional[int]
    renovation: Optional[str]
    ceiling_height_str: Optional[str]
    floors_type: Optional[str]
    walls_type: Optional[str]

    metro_station: Optional[str]
    metro_distance: Optional[int]
    metro_color: Optional[str]

    ceiling_height: Optional[float]
    flatinfo_url: Optional[str]

    @validator('ceiling_height', always=True)
    def convert_value_to_meters(cls, v, values):
        height = values.get('ceiling_height_str')
        if height is None:
            return None
        return int(height.split()[0])


class Tender(BaseModel):
    idx: int
    realty_link: str
    image_link: Optional[str]
    realty_type: Optional[str]
    square_meters: Optional[float]
    full_address: str
    address: str
    price: Optional[int]
    price_per_square_meter: Optional[int]
    floors_number: Optional[int]
    floor: Optional[int]
    rooms_number: Optional[int]
    deposit: Optional[int]
    accepting_end_date: Optional[datetime]
    trading_date: Optional[datetime]

    # Из flatinfo
    city: Optional[str]
    district: Optional[str]
    region: Optional[str]
    metro_station: Optional[str]
    metro_distance: Optional[int]
    building_year: Optional[int]
    renovation: Optional[str]
    ceiling_height: Optional[float]
    floors_type: Optional[str]
    walls_type: Optional[str]
    metro_color: Optional[str]
    flatinfo_url: Optional[str]


class TenderBuilder:
    @staticmethod
    def build(flatinfo, invest):
        tender = Tender.construct(
            idx=invest.id,
            realty_link=invest.url,
            image_link=invest.image_url,
            realty_type=invest.object_type_name,
            square_meters=invest.object_area,
            full_address=invest.address,
            address=invest.clean_address,
            price=invest.start_price,
            price_per_square_meter=invest.price_per_square,
            floors_number=invest.floors,
            floor=invest.room_floors,
            rooms_number=invest.rooms_count,
            deposit=invest.deposit,
            accepting_end_date=invest.request_end_date,
            trading_date=invest.tender_date,
            city=flatinfo.city,
            district=flatinfo.district,
            region=flatinfo.region,
            metro_station=flatinfo.metro_station,
            metro_distance=flatinfo.metro_distance,
            building_year=flatinfo.building_year,
            renovation=flatinfo.renovation,
            ceiling_height=flatinfo.ceiling_height,
            floors_type=flatinfo.floors_type,
            walls_type=flatinfo.walls_type,
            metro_color=flatinfo.metro_color,
            flatinfo_url=flatinfo.flatinfo_url,
        )
        return tender
