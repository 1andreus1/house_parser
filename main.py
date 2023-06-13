from models.filter_models import parse_url
from parser import Parser

if __name__ == '__main__':
    url = 'https://investmoscow.ru/tenders?pageNumber=1&pageSize=10'
    params = parse_url(url)

    parser = Parser()
    tenders = parser.run(params)

    for tender in tenders:
        print(tender)
