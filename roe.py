# coding: utf-8
import tushare as ts
import csv
import pandas as pd

year = 2018
season = 3
folderpath = '/Users/zhaomengshuai/Desktop/tushare/'

#### 成长能力 ####
#净资产增长率 nav
#净利润增长率 nprg
#主营业务收入增长率 mbrg
filename1 = folderpath +'data1.csv'
# data1 = ts.get_growth_data(year,season)
# data1.to_csv(filename1,encoding = 'utf_8_sig')
# #目标股票：nav>15 & nprg>0 & mbrg>0
df1 = pd.read_csv(filename1)
outdf1 = df1[(df1['nprg'] > 0) & (df1['mbrg'] > 0)]
outdf1 = outdf1.drop(outdf1.columns[0], axis = 1)
outdf1.to_csv(folderpath + 'outdata1.csv', index = False, encoding = 'utf_8_sig')
out1 = pd.read_csv(folderpath + 'outdata1.csv')

#### 偿债能力 ####
#股东权益比率 sheqratio
#负债率=1-股东权益比率=1-sheqratio
filename2 = folderpath + 'data2.csv'
# #data2 = ts.get_debtpaying_data(year,season)
# #data2.to_csv(filename2,encoding = 'utf_8_sig')
# #目标股票 1-sheqratio <60, 即sheqratio>40
df2 = pd.read_csv(filename2)
outdf2 = df2[df2['sheqratio'] > 40]
outdf2 = outdf2.drop(outdf2.columns[0], axis = 1)
outdf2.to_csv(folderpath + 'outdata2.csv', index = False, encoding = 'utf_8_sig')
out2 = pd.read_csv(folderpath + 'outdata2.csv')

#### 股票基本情况 ####
#市盈率 pe
filename3 = folderpath + 'data3.csv'
# data3 = ts.get_stock_basics()
# data3.to_csv(filename3, encoding = 'utf_8_sig')
# #目标股票 pe<30
df3 = pd.read_csv(filename3)
outdf3 = df3[df3['pe'] < 30]
outdf3.to_csv(folderpath + 'outdata3.csv', index = False, encoding = 'utf_8_sig')
out3 = pd.read_csv(folderpath + 'outdata3.csv')

#### 净资产收益率 roe ####
filename4 = folderpath + 'data4.csv'
#data4 = ts.get_report_data(year, season)
#data4.to_csv(filename4, encoding = 'utf_8_sig')
# 目标股票 roe > 15

df4 = pd.read_csv(filename4)
outdf4 = df4[df4['roe'] > 15]
outdf4 = outdf4.drop(outdf4.columns[0], axis = 1)
outdf4.to_csv(folderpath + 'outdata4.csv', index = False, encoding = 'utf_8_sig')
out4 = pd.read_csv(folderpath + 'outdata4.csv')

##### 筛选出的目标股票 ####
targetdf = pd.merge(out1, out2, on = 'code', how='inner')
targetdf1 = pd.merge(targetdf,out3, on = 'code', how = 'inner')
targetdf2 = pd.merge(targetdf1,out4, on = 'code', how = 'inner')
targetdf2.to_csv(folderpath + 'target.csv', index = False, encoding = 'utf_8_sig')
sortdf = pd.read_csv(folderpath + 'target.csv')

# #### 排序by nav/((1-sheqratio)*pe) ####
sortdf['zms'] = sortdf['roe']/((100-sortdf['sheqratio'])*sortdf['pe'])
sortdf = sortdf.sort_values('zms',ascending = False)
sortdf = sortdf[['code','name_x','roe', 'sheqratio','pe','nprg','mbrg','zms']]
sortdf = sortdf.drop_duplicates('code')
sortdf.to_csv(folderpath + 'target-sort.csv', index = False, encoding = 'utf_8_sig')
