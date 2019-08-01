# django_intranet_base
Base para generar una intranet utilizando Django y AdminLTE 3

# Instalación

Al descargar el proyecto encontraremos un archivo llamado "requirements.txt" el cual contiene todas las dependencias Python para ejecutar el proyecto. 

Ejecutamos lo siguiente: 

    $ pip install -r requirements.txt

# Configuración.

Cree una copia del archivo "settings.example.json" con el nombre "settings.json".

Una vez realizado esto, deberá configurar la información de las credenciales de su base de datos

    "DB": {
        "default": {
          "ENGINE": "django.db.backends.postgresql_psycopg2",
          "HOST": "localhost",
          "NAME": "django_intranet_base",
          "USER": "admin",
          "PASSWORD": "admin",
          "PORT": 5432
        }
      }


Y también sus credenciales de envío de correos electrónicos. 

    "EMAIL": {
        "EMAIL_USE_TLS": true,
        "EMAIL_HOST": "smtp.gmail.com",
        "EMAIL_PORT": 587,
        "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "EMAIL_HOST_USER": "my-mail@gmail.com",
        "EMAIL_HOST_PASSWORD": "**************",
        "DEFAULT_FROM_EMAIL": "my-mail@gmail.com",
        "CONTACT_EMAIL": "my-mail@gmail.com"
    }

# Iniciando base de datos y proyecto.

Ejecutamos las migraciones para crear la base de datos: 

    $ python manage.py migrate


y posteriormente generamos nuestro super usuario. 

    $ python manage.py createsuperuser


Listo! Esto debe ser todo lo necesario para que tengan corriendo el proyecto en sus equipos locales: 

    $ python manage.py runserver
