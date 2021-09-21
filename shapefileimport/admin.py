from django.contrib import admin
from .models import ShapeImports
from .shapetasks import loadShape, ImportShapeFile
from django.db import connection
import os

class ShapeImportsAdmin(admin.ModelAdmin):
    list_display = ('shapename', 'filename')

    def save_model(self, request, obj, form, change):
        obj.djangoUser = request.user
        obj.save()
        file = request.FILES
        shapemodel = ImportShapeFile(file['filename'], request.user, obj.id)
        ShapeImports.objects.filter(pk=obj.id).update(shapemodel=shapemodel[0], shapetable=shapemodel[1],
                                                            shapename=shapemodel[2])
        deleteorigin = obj.deletefile
        if deleteorigin is True:
            orf = 'shapefileimport/uploads/' + str(file['filename'])
            os.remove(orf)

    def delete_queryset(self, request, queryset):
        for shape in queryset.iterator():
            table = 'shapefileimport_' + str(shape.shapetable)
            SQL = "DROP TABLE " + table + ";"
            with connection.cursor() as cursor:
                cursor.execute(SQL)
        queryset.delete()

admin.site.register(ShapeImports, ShapeImportsAdmin)