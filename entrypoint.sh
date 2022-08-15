python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
#gunicorn project.wsgi:application --bind 0.0.0.0:8000
