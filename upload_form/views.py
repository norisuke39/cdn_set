# Create your views here.
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.conf import settings
from upload_form.models import FileNameModel
import sys, os
UPLOADE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/files/'

def form(request):
    if request.method != 'POST':
        return render(request, 'upload_form/form.html')

    file = request.FILES['file']
    path = os.path.join(UPLOADE_DIR, file.name)
    destination = open(path, 'wb')
    
    reader = csv.reader(file)
    #columns = file.columns

    for chunk in file.chunks():
        destination.write(chunk)

    insert_data = FileNameModel(file_name = file.name)
    insert_data2 = FileNameModel(columns_name = file.columns)
    insert_data.save()

    return redirect('upload_form:complete')

def complete(request):
    return render(request, 'upload_form/complete.html')