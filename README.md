# Интернет-магазин на FastAPI

Простой RESTful API для интернет-магазина.

## Как запустить проект

Скачать удаленный репозиторий выполнив команду

```
git clone https://github.com/AlekseiTolchin/ecommerce_project
```

В корневой директории проекта создать файл `.env` со следующими настройками:

- `POSTGRES_DB`= название базы данных
- `POSTGRES_USER`= имя пользователя
- `POSTGRES_PASSWORD`= пароль
- `POSTGRES_HOST`= имя хоста
- `POSTGRES_HOST`= номер порта
- `JWT_SECRET_KEY`= генерируется с помощью `openssl`, командой `openssl rand -hex 32`
- `JWT_ALGORITHM`= алгоритм шифрования, например `HS256`

Запустить команды:

```
docker-compose build
```

```
docker-compose up
```

Ссылки для тестирования:

http://127.0.0.1:8000/api/docs/ - `документация API`  
