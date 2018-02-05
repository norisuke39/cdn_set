from django.db import models

# Create your models here.
from datetime import datetime

class FileNameModel(models.Model):
    file_name = models.CharField(max_length = 50)
    upload_time = models.DateTimeField(default = datetime.now)
    file_obj = models.FileField(upload_to = 'upload_form/static/files/')
    
class ImageURLModel(models.Model):
    image_url_name = models.URLField()
    upload_time = models.DateTimeField(default = datetime.now)
    
class BudgetModel(models.Model):
    budget = models.IntegerField()