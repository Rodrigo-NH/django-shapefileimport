# Django-shapefileimport

GeoDjango includes a helper function to import ESRI shapefiles to PostGIS enabled DB:  [LayerMapping]
It works as intended but it's still a boring process. Moreover, the usual importing procedure means creating new migrations for each imported shapefile. This is problably OK for sparse importings of a couple of shapefiles. But as I needed to manage many shapefiles and/or keep adding/deleting them it doesn't sounded to me very sane to keep afecting migration files (and migration history).
This APP proposes an alternative to manage such shapefiles:
- Adds shapefile ZIP import option in admin page. Imports will include feature fields.
- Loads shapefiles by name on demand without touching migrations (so you can use all nice GeoDjango API features)
- Delete shapefiles from admin panel
- Option to keep or discard uploaded ZIP files while importing to DB

## Installation
Clone this repo:
```sh
git clone https://github.com/Rodrigo-NH/django-shapefileimport
```
Enter the 'django-shapefileimport' directory, install de dependencies, enter shell and start a new project (For simplicity I reccomend keeping the ending dot at the django-admin startproject command, it makes project folder to be created at same level as the APP [not nested])
```sh
pipenv install
pipenv shell
django-admin startproject mysite .
```
edit './mysite/settings.py' and add to INSTALLED_APPS:
```sh
'django.contrib.gis',
'shapefileimport'
```
Still at './mysite/settings.py', configure the database connection:
```py
DATABASES = {
'default': {
'ENGINE': 'django.contrib.gis.db.backends.postgis',
'NAME': 'shapeimportsDB',
'USER': 'geo',
'HOST': '192.168.0.40',
'PORT': '5432',
'PASSWORD': 'dbpassword',
#'CONN_MAX_AGE': 0,
},
}
```
Run migrations, create superuser and start the APP:
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
It must be done at this point. Enter admin panel and start importing your shapefiles.
After importing, use 'loadShape()' function to load the shapefile and use. Example:
```sh
from shapefileimport.shapetasks import loadShape
from django.core.serializers import serialize
ds = loadShape('MyShapeName')
ff = serialize('geojson', ds.objects.all(), geometry_field='geom',)
```

## Notes
- You must have a propper GeoDjango setup environment, refer to https://docs.djangoproject.com/en/3.2/ref/contrib/gis/
- You must have PostGIS enabled, refer to https://postgis.net/install/
- This APP uses GeoDjango's LayerMapping helper to extract fields among other operations
- Only tested against PostreSQL

[LayerMapping]: https://docs.djangoproject.com/en/3.2/ref/contrib/gis/layermapping/
