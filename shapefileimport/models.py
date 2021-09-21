from django.contrib.gis.db import models
from django.contrib.auth.models import User

# Create your models here.
class ShapeImports(models.Model):
    id = models.AutoField(primary_key=True)
    djangoUser = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    filename = models.FileField (upload_to='shapefileimport/uploads', verbose_name='ZIP file containing .shp .shx .prj .dbf .cpg')
    shapemodel = models.JSONField(null=True, editable=False)
    shapetable = models.CharField(max_length=150, null=False, editable=False)
    # landMark = models.TextField(blank=True)
    shapename = models.CharField(max_length=150, null=False, editable=False, verbose_name='ShapeFile Name')
    deletefile = models.BooleanField(default=False, verbose_name='Delete uploaded file after importing to DB')

    class Meta:
        verbose_name_plural = "Shape imports"

