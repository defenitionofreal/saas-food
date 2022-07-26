python manage.py makemigrations --noinput
python manage.py migrate --noinput
#python manage.py runprofileserver --use-cprofile --prof-path=/tmp/prof/
python manage.py runserver 0.0.0.0:8000
# gunicorn project.wsgi:application --bind 0.0.0.0:8000
