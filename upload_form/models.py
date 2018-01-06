from django.db import models

# Create your models here.
from datetime import datetime

class FileNameModel(models.Model):
    file_name = models.CharField(max_length = 50)
    upload_time = models.DateTimeField(default = datetime.now)
    columns_name = models.CharField(max_length = 50)