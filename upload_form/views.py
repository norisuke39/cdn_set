# Create your views here.
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.conf import settings
from upload_form.models import FileNameModel
from upload_form.models import ImageURLModel
from upload_form.models import BudgetModel
import sys, os
import pandas as pd
from . import forms as forms
from . import calculate as cl
from django import forms as fm_d
UPLOADE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/files/'

###ファイルアップロード関数
def form(request):
    
    #通常時form.htmlを表示
    if request.method != 'POST':
        return render(request, 'upload_form/form.html')
    
    #ファイル取得し、データをcsv_dataに格納
    file = request.FILES['file']
    path = os.path.join(UPLOADE_DIR, file.name)
    destination = open(path, 'wb')
    
    '''#Fileをアップロード先に保存
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()'''
    
    #File名をサーバーに保存
    insert_data = FileNameModel(file_name = file.name,file_obj = file)
    insert_data.save()
    
    return redirect('upload_form:choice_column')
    #return render(request,'upload_form/complete.html',data)


###ファイルアップロード完了関数
def complete(request):
    
    return render(request, 'upload_form/complete.html')

###アップしたファイルのカラム名からアロケしたい要素を選択
def choice_column(request):
    
    #データベースに格納されたファイルオブジェクトを抽出→URLを抽出→ファイルデータを格納
    temp = FileNameModel.objects.latest('id')
    csv_data = pd.read_csv(temp.file_obj.url, encoding = 'ms932')

    #選択されたファイルのカラム名をリスト化(アロケ粒度用)
    group1 = []
    for factor in csv_data.select_dtypes(exclude=['number']).columns:
        group1.append((factor,factor))
        
    #選択されたファイルのカラム名をリスト化(Day選択用)
    group2 = []
    for factor in csv_data.select_dtypes(exclude=['number']).columns:
        group2.append((factor,factor))          
        
    #選択されたファイルのカラム名をリスト化(最大化項目選択用)
    group3 = []
    for factor in csv_data.select_dtypes(include=['number']).columns:
        group3.append((factor,factor))  
        
    #選択されたファイルのカラム名をリスト化(入力項目選択用)
    group4 = []
    for factor in csv_data.select_dtypes(include=['number']).columns:
        group4.append((factor,factor))

    #forms.pyで定義されたフォームをファイルのカラム名で再定義
    form = forms.DfColumnForm()
    form.fields['df_columns'].choices = group1
    form.fields['df_date'].choices = group2
    form.fields['df_goal'].choices = group3
    form.fields['df_control'].choices = group4

    #選択されたカラム名/date項目を受け取り
    obj_choices = request.POST.getlist('df_columns')
    obj_date = request.POST.getlist('df_date')
    obj_goal = request.POST.getlist('df_goal')
    obj_control = request.POST.getlist('df_control')
    
    image_url = ''

    ###計算結果
    if obj_choices:
        obj_budget = request.POST['df_budget']
        insert_budget = BudgetModel(budget = obj_budget)
        insert_budget.save()
        result,images,result_file_name = cl.calculate(obj_choices,obj_date,obj_goal,obj_control,int(obj_budget))
        ##シミュレーション結果をデータベースへ保存
        insert_data_image = ImageURLModel(image_url_name = result_file_name)
        insert_data_image.save()

        return redirect('upload_form:result')
    else:
        obj_budget = ''
        result = ''
        images = ''
        budget_for_print = ''

    data = {
        'input_data' : form,
        'budget_for_print' : budget_for_print,
    }
    
    return render(request,'upload_form/choice_column.html',data)

def result(request):
    
    temp = ImageURLModel.objects.latest('id')
    csv_data = pd.read_csv(temp.image_url_name, encoding = 'utf-8')   
    '''excel = pd.ExcelFile(temp.image_url_name,encoding = 'ms932')
    sheet_name = excel.sheet_names
    csv_data= excel.parse()'''
    images = csv_data['graph_url']
    image_names = csv_data['graph_name']
    
    budget = BudgetModel.objects.latest('id')
    data = {
            'images' : images,
        'image_names' : image_names,
            'budget' : budget.budget,
        
    }
    
    return render(request,'upload_form/result.html',data)