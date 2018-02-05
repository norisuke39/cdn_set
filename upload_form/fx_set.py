# encoding: utf-8

import numpy as np
import pandas as pd

def allocate_by_pattern(_data, _col):

    _data_obj = _data.select_dtypes(include=['object'])
    _data_num = _data.select_dtypes(include=['number']).fillna(0)
    _data_dat = _data.select_dtypes(include=['datetime'])

    _col_obj = _data_obj.columns
    _col_num = _data_num.columns
    _col_dat = _data_dat.columns

    _data = _data[_col + list(_col_dat) + list(_col_num)]

    _element_list = np.array(_data[_col])
    _unique_list = np.vstack({tuple(row) for row in _element_list})

    data_rsp = pd.DataFrame(columns=[])

    data_wk = _data.groupby(_col + list(_col_dat),as_index = False).sum().fillna(0)
    for row in _unique_list:
        mask = np.array(data_wk[_col]) == row
        mask = np.prod(mask, axis=1).astype(np.bool)
        data_wk_result = data_wk[mask].dropna()

        
