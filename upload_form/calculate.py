import numpy as np
import pandas as pd
import scipy.stats 
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg') # 追加
import matplotlib.pyplot as plt
from operator import itemgetter
import json
import itertools
from upload_form.models import FileNameModel
from upload_form.models import ImageURLModel
from . import allocation as al
ROOP = 10 ##アロケーションアルゴリズムの試行数

def calculate(_col,date,goal,control,budget_all):
    ##ファイル読み込み
    file = FileNameModel.objects.latest('id')
    _data = pd.read_csv(file.file_obj.url, encoding = 'ms932')
    ##欠損値除去
    _data = _data.replace(np.NaN,0)
    ##計算方法の選択
    calc_method = 2 ##1:ax*b 2:a*log+b 3:a*arctan+b

    ##変数選択
    X_axis = control[0] #X軸のMeasurement
    Y_axis = goal[0] #Y軸のMeasurement
    
    #説明変数が0の時は除外
    _data = _data[_data[X_axis] != 0]
    
    ##対数回帰関数定義##
    #線形回帰
    if calc_method == 1:
        def linear_fit(x,a,b):
            return a*x+b
    #対数回帰
    if calc_method == 2:
        def log_fit(x,a,b):
            return a*np.log(x)+b
    #arctan()回帰
    if calc_method == 3:
        def arctan_fit(x,a,b):
            return a*np.arctan(x)+b

    _data_obj = _data.select_dtypes(include=['object'])
    _data_num = _data.select_dtypes(include=['number']).fillna(0)
    _data_dat = date

    _col_obj = _data_obj.columns
    _col_num = _data_num.columns
    _col_dat = _data_dat

    _data = _data[_col + list(_col_dat) + list(_col_num)]

    _element_list = np.array(_data[_col])
    _unique_list = np.vstack({tuple(row) for row in _element_list})

    data_rsp = pd.DataFrame(columns=[])
    data_stat = pd.DataFrame(columns = [])

    data_wk = _data.groupby(_col + list(_col_dat),as_index = False).sum().fillna(0)
    
    for row in _unique_list:
        mask = np.array(data_wk[_col]) == row
        mask = np.prod(mask, axis=1).astype(np.bool)
        data_set_pattern = data_wk[mask].dropna()
        data_set_pattern = data_set_pattern.sort_values(X_axis,ascending = False)

        if len(data_set_pattern) > 1:
            ##非線形回帰式によるパラメータ推定
            if calc_method == 1:
                param,cov = curve_fit(linear_fit,data_set_pattern[X_axis],data_set_pattern[Y_axis])
                data_fit = linear_fit(data_set_pattern[X_axis],param[0],param[1])
            if calc_method == 2:
                param,cov = curve_fit(log_fit,data_set_pattern[X_axis],data_set_pattern[Y_axis])
                data_fit = log_fit(data_set_pattern[X_axis],param[0],param[1])
            if calc_method == 3:
                param,cov = curve_fit(arctan_fit,data_set_pattern[X_axis],data_set_pattern[Y_axis])
                data_fit = arctan_fit(data_set_pattern[X_axis],param[0],param[1])

            ##決定係数算出
            cor = scipy.stats.pearsonr(data_fit, data_set_pattern[Y_axis])
            #print('決定係数:{0}%'.format(int(cor[0]*cor[0]*100)))

            ##MAPE値算出
            data_set_pattern2 = data_set_pattern[data_set_pattern[Y_axis] != 0]
            data_fit2 = data_fit[data_set_pattern[Y_axis] != 0]
            MAPE = abs(data_fit2 - data_set_pattern2[Y_axis])/data_set_pattern2[Y_axis]
            if len(MAPE) == 0:
                MAPE = 0
            else:
                MAPE = MAPE.sum()/len(MAPE)
            #print('MAPE:{0}%'.format(int(MAPE*100)))

            ##グラフ描画    
            #print(row)
            fig,ax = plt.subplots()
            ax.scatter(data_set_pattern[X_axis],data_set_pattern[Y_axis])

            ##推定値グラフ描画
            ax.plot(data_set_pattern[X_axis],data_fit,color = "orange")
            #print(param)

            ##グラフ描画実行##
            #plt.grid(True)
            #plt.show()
            ##モデルデータ要素格納
            for (i,j) in zip(_col,row):
                data_rsp[i] = pd.Series(j)
            data_rsp['coe'] = param[[0]]
            data_rsp['inter'] = param[[1]]
            data_rsp['R^2'] = cor[0]*cor[0]
            data_rsp['MAPE'] = MAPE*100
            data_rsp['graph_name'] = '_'.join(row) + '.jpg'
            data_rsp['graph_url'] = '/static/upload_form/'+'_'.join(row) + '.jpg'
            data_stat = data_stat.append(data_rsp)
            plt.savefig('./static/upload_form/'+'_'.join(row) +'.jpg')

    ###アロケーション
    data_result = al.Allocation(budget_all,data_stat)

    ###ファイル保存
    result_file_name = 'planning_result.csv'
    data_result.to_excel('planning_result.xlsx',index = False)
    data_result.to_csv(result_file_name,index = False)
    
    return data_result,data_result['graph_url'],result_file_name