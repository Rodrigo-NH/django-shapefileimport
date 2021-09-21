from django.contrib.gis.utils import LayerMapping
from .models import ShapeImports
from django.contrib.gis.db import models
from django.apps import apps
from django.core.management import call_command
from django.db import connections
import os
import zipfile

def ImportShapeFile(f, user, shpID):
    shp = 'shape_'+str(user.id)+'_'+str(shpID)
    fl = []
    shapename = ""
    with zipfile.ZipFile(f, 'r') as zip_ref:
        zipFiles = zip_ref.namelist()
        for target_file in zipFiles:
            extens = target_file.split(target_file[:-4])[1]
            if extens.upper() == ".SHP":
                shapename = target_file[:-4]
            fn = 'shapefileimport/uploads/'+shp+extens.upper()
            fl.append(fn)
            with open(fn, "wb") as f:
                f.write(zip_ref.read(target_file))
    shpf='shapefileimport/uploads/'+shp+'.SHP'
    ba = call_command('ogrinspect', shpf, shp, '--multi-geom', '--mapping', '--null=True')
    bas = ba.splitlines()
    ct = 0
    fields = {}
    mapp = {}
    for each in bas:
        dd = each.strip()
        if "LayerMapping" in dd:
            ct = 1
        if ct == 0:
            if "= models." in dd and "ID =" not in dd.upper():
                dd1 = dd.split(" = ")
                fields[dd1[0]] = dd1[1]
        if ct == 1:
            if "':" in each and "ID" not in each.upper():
                tt = each.replace("'","").split(",")[0].split(":")
                mapp[tt[0].strip()] = tt[1].strip()
    fieldsObject = fieldObjetify(fields)
    ModelName = type(shp, (models.Model,), fieldsObject )
    with connections['default'].schema_editor() as schema_editor:
        schema_editor.create_model(ModelName)
    lm = LayerMapping(ModelName, shpf, mapp, transform=False)
    lm.save(strict=True, verbose=False)
    for each in fl:
        os.remove(each)
    return [ fields, shp, shapename, f ]

def loadShape(shapename):
    """
    Load ESRI shape from database. Check if related unmanaged model is registered already and register it if not loaded previously.
    Return the desired shapefile table model
    example: 'desiredmodel = loadShape('UFEBRASIL_WGS84')'
    """
    tt = ShapeImports.objects.filter(shapename=shapename).get()
    fields = fieldObjetify(tt.shapemodel)
    table = tt.shapetable
    desiredmodel = None
    app_models = apps.get_app_config('shapefileimport').get_models()
    allmodels = []
    for model in app_models:
        if model._meta.verbose_name == table:
            desiredmodel = model
        allmodels.append(model._meta.verbose_name)
    if table not in allmodels:
        desiredmodel = type(table, (models.Model,), fields)
    return desiredmodel

def fieldObjetify(fields):
    outFields = {}
    for key in fields:
        outFields[key] = eval(fields[key])
    outFields['__module__'] = 'shapefileimport.shapetasks'
    return outFields