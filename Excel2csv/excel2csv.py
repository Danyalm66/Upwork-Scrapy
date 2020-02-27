import pandas as pd
try:
    data_xls = pd.read_excel('exceltest.xlsx', 'Sheet1', index_col=None)
except IOError:
    data_xls = pd.read_excel('exceltest.xls', 'Sheet1', index_col=None)
    pass
data_xls.to_csv('your_csv.csv', encoding='utf-8')
