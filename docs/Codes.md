virtualenv ven
.\ven\Scripts\activate
pip install -U autopep8
pip install django
django-admin startproject Electric_Board .
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
django-admin startapp EB_App
python manage.py createsuperuser
python manage.py collectstatic




python manage.py makemigrations && python manage.py migrate

.\ven\Scripts\activate && cd src && python manage.py runserver

"terminal.integrated.shellArgs.windows": ["-ExecutionPolicy", "Bypass"]

 python -m smtpd -n -c DebuggingServer localhost:1025

 ctrl+shift+.
 ctrl+ p >,#
crtl + g
crtl + d
crtl + d * 3 times

alt + |^ (upper arrow) or (downarrow) for moving
alt + SHIFT + |^ (upper arrow) or (downarrow) FOR COPYING and moving
crtl + L for highlighting line

<!-- Setting.py changes -->
    import os

    INSTALLED_APPS = [
        "EB_App",
    ]

    'DIRS': [os.path.join(BASE_DIR, 'templates')],

    TIME_ZONE = 'Asia/Kolkata'

    STATIC_ROOT = os.path.join(BASE_DIR, "static")

<!--  -->