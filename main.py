from models.filter_models import parse_url
from parser import Parser

if __name__ == '__main__':
    url = 'https://investmoscow.ru/tenders?pageNumber=1&pageSize=10&orderBy=RequestEndDate&orderAsc=true&objectTypes=nsi:41:30011566&objectTypes=nsi:41:30011568&objectKinds=nsi:tender_type_portal:13&price.min=1610000&price.max=12000000&tenderStatus=nsi:tender_status_tender_filter:1&objectForms=nsi:45:45001'
    params = parse_url(url)

    parser = Parser()
    tenders = parser.run(params)

    for tender in tenders:
        print(
            tender.flatinfo_url,
            tender.metro_station,
            tender.metro_distance,
            tender.metro_color,
            tender.station_type,
        )
