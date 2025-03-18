# Cистема управления заказами в кафе

### Описание

Необходимо разработать полнофункциональное веб-приложение на Django для управления заказами в кафе. Приложение должно позволять добавлять, удалять, искать, изменять и отображать заказы. Каждый заказ должен содержать следующие поля:
    • id (уникальный идентификатор, генерируется автоматически)
    • table_number (номер стола)
    • items (список заказанных блюд с ценами)
    • total_price (общая стоимость заказа, вычисляется автоматически)
    • status (статус заказа: “в ожидании”, “готово”, “оплачено”)


### Стек
- python - язык разработки
- JavaScript - язык разработки использовался для взаимодействия на фронте
- Django - фреймворк на основе которого создан сервис
- PostgreSQL - БД для хранения информации
- Django REST Framework - фреймворк для написания API

### Запуск
Сперва убедитесь, что установлен [Docker](https://docs.docker.com/engine/install/).
Добавьте переменные окружения в файл .env
```python
DB_NAME = ''
DB_USER = ''
DB_PASS = ''
DB_HOST = ''
DB_PORT = ''
```

```bash
$ docker compose up -d
```

Установите зависимости

```bash
pip install -r requirements.txt
```

Запустите сервер
```bash
python manage.py runserver
```

### Функционал

Приложение поддерживает полное взаимодействие с заказами. Прежде чем создать заказ необходимо открыть смену. 
Смена может быть открыта только одна. Подсчет выручки происходит после закрытия смены. Также имеется страница со всеми сменами.

Для более комфортного и приятного оформления заказов к проекту были написаны JS скрипты для добавления/удаления позиции заказа при оформлении.
Также JS скрипты использовались для строки поиска. В виду ограничения по времени выполнения, не был реализован функционал  всего списка заказа при пустой строке поиска.
Также по этой же причине в проекте отсутствуют тесты.

### О себе
Целеустремленный Python разработчик - альтруист, ищущий оффер мечты.

Занимаюсь разработкой более 2х лет, умею: писать чистый код, проводить code review, взаимодействовать со сторонними API, разрабатывать RESTful API, писать unit тесты, работать в команде, декомпозировать сложные задачи. Также имею 3 года опыта работы в нефтяной и тепловых компаниях,

Реализовал 5 проектов 1 из них коммерческий (парсер для компании АНО "Центр развития"), 1 командный (интернет магазин бытовой техники), 1 для личных целей (телеграмм бот для учета заправленного топлива), остальные учебные.

Выбор нового направления в качестве python разработчика, обусловлен тем, что разработчик творческая и в то же время техническая профессия. Разработка дает возможность делать жизнь проще как для бизнеса, так и для людей.

Telegram: https://t.me/ReBiwer
Github: https://github.com/ReBiwer
