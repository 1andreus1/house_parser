from models.filter_models import parse_url
from parser import Parser

if __name__ == '__main__':
    url = 'https://investmoscow.ru/tenders?pageNumber=1&pageSize=10&orderBy=RequestEndDate&orderAsc=true&objectTypes=nsi:41:30011568&objectTypes=nsi:41:30011566&objectKinds=nsi:tender_type_portal:13&price.min=1900000&price.max=2000000&tenderStatus=nsi:tender_status_tender_filter:1&objectForms=nsi:45:45001'
    params = parse_url(url)

    parser = Parser()
    tenders = parser.run(params)

    for tender in tenders:
        print(tender)

    print('Всего: ', len(tenders))
