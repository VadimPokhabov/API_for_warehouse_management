# API для управления складом
----
 Приложение выполнено на FastAPI
### Стек:
* Python
* FastAPI
* DSQLAlchemy
* Psycopg2-binary
____
### Бизнес-логика:
* При создании заказа проверяет наличие достаточного количества товара на складе.
* Обновляет количество товара на складе при создании заказа (уменьшение доступного количества).
* В случае недостаточного количества товара – возвращает ошибку с соответствующим сообщением.

____
Для запуска проекта у себя локально необходимо:

1. git clone репозитория
```
git@github.com:VadimPokhabov/API_for_warehouse_management.git
```
2. Установить виртуальное окружение venv
```
python3 -m venv venv для MacOS и Linux систем
python -m venv venv для windows
```
3. Активировать виртуальное окружение
```
source venv/bin/activate для MasOs и Linux систем
venv\Scripts\activate.bat для windows
```
4. установить файл с зависимостями
```
pip install -r requirements.txt
```
5. Создать базу данных в PgAdmin, либо через терминал.
6. Заполнить своими данными файл .env в корне вашего проекта. Образец файла лежит в корне .env.sample
7. Для запуска проекта использовать файл 
```
src/main.py
```
Запуск приложения через Docker:

1. Повторить шаги 1-3
2. Запустить Docker локально на машине
3. Выполнить команду в терминале
```
docker-compose up -d --build
```
Данная команда сразу создаст образ, и сбилдит его, т.е. запустит локально в Docker

4. Переходим по ссылке http://localhost:8000/
----
Чтобы удалить контейнеры после работы с приложением используйте команду
```
docker-compose down
```