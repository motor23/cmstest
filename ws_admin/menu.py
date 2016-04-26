from .components.menu import items


menu = {
    'main': [
        items.Url(title='Главная', url='/'),
        items.Item(title='Cобытия', children=[
            items.Stream(title='Новости', stream='news'),
            items.Stream(title='Документы', stream='docs'),
            items.Stream(title='Поездки', stream='visits'),
        ]),
        items.Item(title='Полезные ссылки', children=[
            items.Url(title='Почта', url='http://www.gmail.com'),
            items.Url(
                title='Портал правительства',
                url='http://www.governamnt.ru',
            ),
            items.Url(title='yandex.ru', stream='http://yandex.ru'),
        ]),
    ],
    'dashboard': [
        items.Item(title='Главная страница', children=[
            items.Stream(title='Слайдер', stream='vars', item_id='slider'),
            items.Stream(
                title='Главная фотолента',
                stream='vars',
                item_id='main_photoset',
            ),
            items.Stream(title='Хайлайт', stream='vars', item_id='highlight'),
        ]),
        items.Item(title='События', children=[
            items.Stream(title='Новости', stream='news'),
            items.Stream(title='Документы', stream='docs'),
            items.Stream(title='Поездки', stream='visits'),
        ]),
        items.Item(title='Мультимедия', children=[
            items.Stream(
                title='Фотоленты',
                stream='multimedia',
                filters={'type': 'photset'},
            ),
            items.Stream(
                title='Фото',
                stream='multimedia',
                filters={'type': 'photset'},
            ),
            items.Stream(
                title='Видео',
                stream='multimedia',
                filters={'type': 'video'},
            )
        ]),
    ],
}
