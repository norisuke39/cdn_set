import numpy as np
import pandas as pd
import itertools

#試行数の定義
ROOP = 100

###アロケーションアルゴリズム###
def Allocation(budget,df):
    step_size = 100
    step = budget/step_size
    step_set = [int(i*step_size) for i in range(int(step)+1)]
    pattern = itertools.combinations_with_replacement(step_set,len(df))
    pattern_arr = np.array(list(pattern))
    np.sum(pattern_arr,axis = 1) == budget
    pattern_set = pattern_arr[np.sum(pattern_arr,axis = 1) == budget]
    pattern_all = list()
    for i in range(len(pattern_set)):
        pattern_pro1 = itertools.permutations(pattern_set[i])
        pattern_all = pattern_all+list(set(pattern_pro1))
    
    temp_int = 0
    temp_array = [0]
    for i in pattern_all:
        df['pre_CV'] = df['coe']*i+df['inter']
        if temp_int < int(df['pre_CV'].sum()):
            temp_int = int(df['pre_CV'].sum())
            temp_array = i
    df['pre_cost'] = temp_array
    df['pre_CV'] = (df['coe']*df['pre_cost']+df['inter']).astype(np.int64)
    df['pre_CPA'] = (df[df['pre_CV'] != 0].pre_cost / df[df['pre_CV'] != 0].pre_CV).astype(np.int64)
    return df
'''
###アロケーションアルゴリズム###
def Allocation(budget,df):
    step_size = 100
    step = budget/step_size
    step_set = [int(i*step_size) for i in range(int(step)+1)]
    temp_int = 0
    temp_array = [0]
    for i in range(ROOP):
        df['pre_cost'] = 100*np.random.randint(0,int(step),len(df))
        df['pre_CV'] = df['coe']*df['pre_cost']+df['inter']
        if temp_int < int(df['pre_CV'].sum()):
            temp_int = int(df['pre_CV'].sum())
            temp_array = df['pre_cost']
    df['pre_CV'] = df['coe']*temp_array+df['inter']
    df['pre_CPA'] = df['pre_cost'] / df['pre_CV']
    return df
    '''