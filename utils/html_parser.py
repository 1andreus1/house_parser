from copy import deepcopy
from typing import Optional, Dict

from bs4 import BeautifulSoup

from utils.utils import convert_to_meters

SEARCH_VALUES = {
    'Год постройки': 'building_year',
    'Округ': 'district',
    'Район': 'region',
    'Нас. пункт': 'city',
    'Расселение по реновации': 'renovation',
    'Высота потолков': 'ceiling_height_str',
    'Перекрытия': 'floors_type',
    'Стены': 'walls_type',
}


class TagClasses:
    ROW = 'fi-list-item'
    ROW_VALUE = 'fi-list-item__value'
    ROW_LABEL = 'fi-list-item__label'

    METRO = 'underground'
    METRO_LABEL = 'metro-label'


class HtmlParserBase:
    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.search_dict = deepcopy(SEARCH_VALUES)
        self.result_dict = {}

    def get_value(self, row, label):
        span_tag = row.find(
            'span',
            class_=TagClasses.ROW_VALUE,
        )
        if not span_tag:
            return

        value = span_tag.text.strip()
        key = self.search_dict[label]
        self.result_dict[key] = value
        self.search_dict.pop(label)

    def get_metro_name(self, metro: BeautifulSoup):
        name = metro.next_sibling.text.strip()
        self.result_dict['metro_station'] = name

    def get_metro_color(
            self,
            metro: BeautifulSoup
    ) -> Optional[str]:
        svg_tag = metro.find('svg')
        if not svg_tag:
            return

        style_attr = svg_tag.get('style')
        if not isinstance(style_attr, str):
            return

        _style_attr = style_attr.split(':')
        if len(_style_attr) < 2:
            return

        color = _style_attr[1].strip()
        self.result_dict['metro_color'] = color

    def get_metro_distance(self, metro: BeautifulSoup):
        distance_tag = metro.find(
            'span',
            class_=TagClasses.ROW_VALUE,
        )
        if not distance_tag:
            return

        distance_text = distance_tag.text
        words = distance_text.split()
        cleaned_words = [word.strip() for word in words if word.strip()]
        last_two_words = cleaned_words[-2:]
        distance = ' '.join(last_two_words)

        distance_in_meters = convert_to_meters(distance)
        self.result_dict['metro_distance'] = distance_in_meters


class HtmlParser(HtmlParserBase):
    def __init__(self, html: str):
        super().__init__(html)

    def parse(self) -> Dict:
        self.parse_tables()
        self.parse_metro()
        return self.result_dict

    def parse_tables(self) -> None:
        rows = self.soup.find_all(
            'li',
            class_=TagClasses.ROW
        )
        if not rows:
            return

        for row in rows:
            self.parse_row(row)

    def parse_metro(self) -> None:
        all_metro = self.soup.find(
            'ul',
            class_=TagClasses.METRO
        )
        if not all_metro:
            return

        metro = all_metro.find(
            'li',
            class_=TagClasses.ROW
        )
        if not metro:
            return

        metro_label = metro.find(
            'span',
            class_=TagClasses.METRO_LABEL
        )
        if not metro_label:
            return

        self.get_metro_distance(metro)
        self.get_metro_name(metro_label)
        self.get_metro_color(metro_label)

    def parse_row(self, row):
        span_tag = row.find(
            'span',
            class_=TagClasses.ROW_LABEL
        )
        if not span_tag:
            return

        label = span_tag.text.strip()

        if label in self.search_dict:
            self.get_value(row, label)
