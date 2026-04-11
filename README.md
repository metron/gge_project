# Демо проект
Django + Celery + Валидация + DRF + Postgres + Docker

# Запуск
## Запускаем докер контейнеры
sudo docker compose up --build
## Пока контейнеры работают, запускаем миграции Django и создаём админа в другом окне терминала:
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Страницы
http://127.0.0.1:8000/ - форма добавления сметы со списком ранее добавленных смет и их статусом
http://127.0.0.1:8000/api/estimates - запросы по API
http://127.0.0.1:8000/admin - админка Django
