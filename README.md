# Учебный проект 4-го спринта Python-asyncIO

## Описание проекта
Данный проект представляет из себя веб-сервер. На сервере реализовано несколько эндпоинтов для создания
укороченных ссылок. Кодовая база написана в асинхронном стиле

## Запуск проекта
1. Скачайте и запустите базу данных PostgreSQL
```shell
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```
2. Создайте пользователя postgres
```shell
sudo -u postgres createuser {имя пользователя} --interactive
```
3. Скачайте проекта через git cli
```shell
git clone git@github.com:Fr0stFree/async-python-sprint-4.git
```
4. Перейдите в корень проекта. Запустите виртуальное окружение и установите в него зависимости
```shell
python -m venv venv
python . venv/bin/activate
python pip install -r requirements.txt
```
5. Создайте .env файл в корне проекта на основе .env.example. Укажите данные для авторизации созданного postgres пользователя.
6. Перейдите в папку src/ и выполните миграции
```shell
alembic upgrade head
```
7. Запустите проект
```shell
python main.py
```
8. Для запуска тестов воспользуйтесь командой
```shell
pytest 
```

### Использованные библиотеки и фреймворки:
- FastAPI
- Pydantic
- Alembic
- SQLAlchemy
- Pytest
 