# ImageStore

### Description:
Простой REST API, который позволяет загружать картинки, получать картинки, удалять картинки.
Реализована Аутентификация и композитная контейнеризация.

### Authorization
Авторизация реализована при помощи OAth2 и JWT токенов. Каждый endpoint CRUDа требует валидный токен.

- POST /auth/sign-up/ - Получает на входе login и password. Добавляет пользователя в ДБ. Метод возвращает JSON в виде
словаря с полями: access_token(JWT token), access_type.
- POST /auth/sign-in/ - Получает на входе username и password. Если login и password верны, то метод возвращает JSON в виде
словаря с полями: access_token(JWT token), access_type, иначе выбрасывает ошибку Unauthorized.

### CRUD
- POST /frames/ - Получает на вход картинки в виде массива байтов. Для каждой картинки генерируется uuid, а также фиксируется время,
когда картинка была добавлена, добавляется в ДБ. В minio заливаются принятые картинки с именами (uuid).jpg и кладутся
в корзины с именами, которые соответствуют времени добавления в ДБ, в формате <YYYYMMDD>. Метод возвращает json из массива
, включающий в себя объекты с полями: id, frame_id(номер запроса), name, created_at.
- GET /frames/{frame_id} - Получает на вход номер запроса в виде числа. Метод возвращает json из массива объектов с полями:
id, frame_id, name, created_at, content(картинка в кодировке base64).
- DELETE /frames/{frame_id} - Получает на вход номер запроса в виде числа. Удаляет из ДБ и min.io все картинки, 
соответсвующее номеру запроса. 

### Details
1. Все зависимости фиксируются в poetry.
2. В качестве СУБД выбрана SQLite.
3. Реализовано 100% покрытие unit-тестами.

### Run app
    docker-compose up
Затем перейти на ссылку: http://0.0.0.0:8090/docs, там будет Swagger UI.

### Create venv:
    make venv

### Run tests:
    make test

### Run linters:
    make lint

### Run formatters:
    make format
