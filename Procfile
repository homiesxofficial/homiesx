release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn homiesx_server.wsgi --bind 0.0.0.0:$PORT
