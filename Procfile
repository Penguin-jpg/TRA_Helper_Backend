web: gunicorn TRA_helper_backend.wsgi
release: python manage.py makemigrations --noinput
release: python manage.py migrate --noinput
release: winpty python manage.py createsuperuser --identity_number admin --password password --phone_number 0000000000