# intranet_externos
Sistema dedicado a la publicación de documentos para gremios hípicos

# Instalación

Clonar el repositorio del proyecto en la capeta deseada:
    git clone https://github.com/fbahamondes/intranet_externos

Aseurarse de que se encuentra en la última versión.

Crear un entorno virtual:

    $ virtualenv venv --python=python3

Ejecutamos lo siguiente: 

    $ pip install -r requirements.txt


# Configuración.

Configurar el entorno en el cual se encuentra la aplicación agregando al archivo .batch_profile la siguiente linea.

    export DJANGO_SETTINGS_MODULE=intranet_externos.settings.production

Una vez realizado esto, deberá configurar la información de las credenciales de su base de datos

    "DB": {
        "default": {
          "ENGINE": "django.db.backends.postgresql_psycopg2",
          "HOST": "localhost",
          "NAME": "intranet_externos",
          "USER": "admin",
          "PASSWORD": "admin",
          "PORT": 5432
        }
      }


Y también sus credenciales de envío de correos electrónicos. 

    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'correo-ejemplo@hipodromochile.cl'
    EMAIL_HOST_PASSWORD = 'pass'
    EMAIL_PORT = 587

# Iniciando base de datos y proyecto.

Ejecutamos las migraciones para crear la base de datos: 

    $ python manage.py migrate


y posteriormente generamos nuestro super usuario. 

    $ python manage.py createsuperuser


Listo! Esto debe ser todo lo necesario para que tengan corriendo el proyecto en sus equipos locales: 

    $ python manage.py runserver
