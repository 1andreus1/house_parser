from math import ceil
from typing import Optional

from models.filter_models import FilterParams
from models.models import InvestInfo, FlatInfo, TenderBuilder
from utils.html_parser import HtmlParser
from utils.utils import HTTPMethod, DecodeTo, get_url


class ParserRequests:
    URL_FLATINFO = 'https://flatinfo.ru/services/adres_response.php'
    URL_INVEST = 'https://api.investmoscow.ru/investmoscow/tender/v2/filtered-tenders/searchTenderObjects'
    URL_TENDER = 'https://api.investmoscow.ru/investmoscow/tender/v1/object-info/getTenderObjectInformation'

    def get_page_invest(self, params: dict) -> dict:
        res = get_url(
            HTTPMethod.POST,
            DecodeTo.JSON,
            self.URL_INVEST,
            json=params,
        )
        return res

    def get_deposit_invest(self, params: dict) -> dict:
        res = get_url(
            HTTPMethod.GET,
            DecodeTo.JSON,
            self.URL_TENDER,
            params=params,
        )
        return res

    def get_url_flatinfo(self, params: dict) -> dict:
        res = get_url(
            HTTPMethod.GET,
            DecodeTo.JSON,
            self.URL_FLATINFO,
            params=params,
        )
        return res

    @staticmethod
    def get_page_flatinfo(url: str) -> dict:
        res = get_url(
            HTTPMethod.GET,
            DecodeTo.TEXT,
            url,
        )
        return res


class Parser(ParserRequests):
    PAGE_SIZE = 10

    def __init__(self):
        self.params = None
        self.address_cache = {}
        self.url_cache = {}

    def run(self, params: FilterParams):
        self.params: FilterParams = params
        self.params.page_size = self.PAGE_SIZE
        self.address_cache = {}
        self.url_cache = {}

        end_page_number = self._get_end_page_number()
        all_tenders = []

        for page_number in range(1, end_page_number):
            tenders_found = self._get_page_data(page_number)
            cleaned_tenders = self.clear_entities(tenders_found)
            all_tenders.extend(cleaned_tenders)

        obj_tenders = []
        for tender in all_tenders:
            obj_tender = self.construct_tender(tender)
            if obj_tender is not None:
                obj_tenders.append(obj_tender)

        return obj_tenders

    def _get_page_data(self, page_number: int):
        self.params.page_number = page_number
        params = self.params.dict(
            by_alias=True,
            exclude_none=True
        )

        res = self.get_page_invest(params)
        return res

    def clear_entities(self, tenders: dict):
        entities = tenders.get('entities')
        if entities is None:
            return []

        cleaned_tenders = []

        for entity in entities:
            tenders = self.clear_tenders(entity)
            cleaned_tenders.extend(tenders)

        return cleaned_tenders

    @staticmethod
    def clear_tenders(entity):
        tenders = entity.get('tenders')
        if tenders is None:
            return []

        cleaned_tenders = []
        for tender in tenders:
            address = tender.get('address')
            if 'московская обл' not in address.lower():
                cleaned_tenders.append(tender)

        return cleaned_tenders

    def _get_end_page_number(self) -> int:
        count_buildings = self._get_page_data(1)['totalCount']
        end_page_number = ceil(count_buildings / self.PAGE_SIZE) + 1
        return end_page_number

    def _get_tender_detail(self, tender_id: int):
        params = {
            "tenderId": tender_id
        }
        res = self.get_deposit_invest(params)
        return res

    def get_deposit(self, tender_detail: dict) -> Optional[int]:
        procedure_info = tender_detail.get('procedureInfo')
        if not procedure_info:
            return

        for info in procedure_info:
            deposit = self.find_deposit_value(info)

            if deposit:
                return deposit
        return

    @staticmethod
    def find_deposit_value(info):
        label = info.get('label')
        if not isinstance(label, str):
            return

        if label == 'Размер задатка':
            deposit_text = info.get('value')
            if not isinstance(deposit_text, str):
                return

            d_without_comma = deposit_text.split(',')[0]
            deposit = ''.join(d_without_comma.split())

            return int(deposit)

        return

    def get_url_by_address(self, address):
        params = {
            'term': address
        }
        res = self.get_url_flatinfo(params)
        url = res.get('url')
        if url:
            return url

    def construct_tender(self, invest):
        try:
            invest_info = InvestInfo.parse_obj(invest)

            tender_id = invest_info.id
            tender_detail = self._get_tender_detail(tender_id)
            deposit = self.get_deposit(tender_detail)
            invest_info.deposit = deposit

            flat_info = self.get_flatinfo(invest_info.clean_address)
            tender_obj = TenderBuilder.build(flat_info, invest_info)
            return tender_obj
        except (Exception,):
            return

    def get_flatinfo(self, address):
        if address in self.address_cache:
            flat_info = self.address_cache[address]
        else:
            url = self.get_url_by_address(address)
            flat_info = self.get_flatinfo_by_url(url)
            self.address_cache[address] = flat_info

        return flat_info

    def get_flatinfo_by_url(self, url):
        if url in self.url_cache:
            flat_info = self.url_cache[url]
        else:
            text_page = self.get_page_flatinfo(url)
            page = HtmlParser(text_page)
            page_dict = page.parse()
            flat_info = FlatInfo.parse_obj(page_dict)
            flat_info.flatinfo_url = url
            self.url_cache[url] = flat_info

        return flat_info
