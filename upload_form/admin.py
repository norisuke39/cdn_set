# Register your models here.
from django.contrib import admin
from upload_form.models import FileNameModel
from upload_form.models import ImageURLModel
from upload_form.models import BudgetModel

class FileNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'upload_time','file_obj')
    list_display_links = ('id', 'file_name')
    
class ImageURLAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_url_name', 'upload_time')
    list_display_links = ('id', 'image_url_name')
    
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'budget')
    list_display_links = ('id', 'budget')

admin.site.register(FileNameModel, FileNameAdmin)
admin.site.register(ImageURLModel, ImageURLAdmin)
admin.site.register(BudgetModel, BudgetAdmin)