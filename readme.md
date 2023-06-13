# Парсер тендеров
___
## Установка
Чтобы установить необходимые пакеты, выполните следующую команду:
`pip install -r requirements.txt`
___
## Запуск кода

Чтобы запустить код, просто выполните следующую команду:
`python main.py`
___
## Пример кода для запуска

```python
from models.filter_models import parse_url
from parser import Parser

if __name__ == '__main__':
    url = 'https://investmoscow.ru/tenders?pageNumber=1&pageSize=10'
    params = parse_url(url)

    parser = Parser()
    tenders = parser.run(params)

    for tender in tenders:
        print(tender)
```
___
## Описание кода

Код в  `main.py`  парсит заданный URL и извлекает информацию о тендерах на недвижимость. Извлеченные данные выводятся в
консоль. Собираются следующие поля:

| Поле                   | Тип                | Описание                                                          | 
|------------------------|--------------------|-------------------------------------------------------------------| 
| idx                    | int                | Уникальный идентификатор тендера                                  | 
| realty_link            | str                | Ссылка на страницу объекта недвижимости                           | 
| image_link             | Optional[str]      | Ссылка на изображение объекта недвижимости                        | 
| realty_type            | Optional[str]      | Тип объекта недвижимости                                          | 
| square_meters          | Optional[float]    | Площадь объекта недвижимости в квадратных метрах                  | 
| full_address           | str                | Полный адрес объекта недвижимости                                 | 
| address                | str                | Адрес объекта недвижимости без уточнений                          | 
| price                  | Optional[int]      | Начальная цена тендера                                            | 
| price_per_square_meter | Optional[int]      | Цена за квадратный метр объекта недвижимости                      | 
| floors_number          | Optional[int]      | Количество этажей в здании                                        | 
| floor                  | Optional[int]      | Этаж, на котором расположен объект недвижимости                   | 
| rooms_number           | Optional[int]      | Количество комнат в объекте недвижимости                          | 
| deposit                | Optional[int]      | Размер залога                                                     | 
| accepting_end_date     | Optional[datetime] | Дата окончания приема заявок                                      | 
| trading_date           | Optional[datetime] | Дата проведения аукциона                                          | 
| city                   | Optional[str]      | Город, в котором находится объект недвижимости                    | 
| district               | Optional[str]      | Район города, в котором находится объект недвижимости             | 
| region                 | Optional[str]      | Регион, в котором находится объект недвижимости                   | 
| metro_station          | Optional[str]      | Название ближайшей станции метро                                  | 
| metro_distance         | Optional[int]      | Расстояние от объекта недвижимости до ближайшей станции метро     | 
| building_year          | Optional[int]      | Год постройки здания                                              | 
| renovation             | Optional[str]      | Реновация                                                         | 
| ceiling_height         | Optional[float]    | Высота потолков в здании                                          | 
| floors_type            | Optional[str]      | Тип перекрытий в здании                                           | 
| walls_type             | Optional[str]      | Материал стен здания                                              | 
| metro_color            | Optional[str]      | Цвет линии метро, на которой находится ближайшая станция метро    | 
| flatinfo_url           | Optional[str]      | Ссылка на страницу с подробной информацией о объекте недвижимости | 
| station_type           | Optional[str]      | Тип станции метро                                                 |

___