#!/usr/bin/env python
# coding: utf-8

# In[33]:


import fitz
import glob
import re
import requests
import time


#変数を増やすときは辞書を追加する########################
company_n_emp_total = {}
company_n_emp_m = {}
company_n_emp_w = {}
company_age_total = {}
company_age_m = {}
company_age_w = {}
company_length_total = {}
company_length_m = {}
company_length_w = {}
company_sal = {}
company_new = {}
company_mid = {}
company_stay1_m = {}
company_stay1_w = {}
company_stay2 = {}
company_leave_m = {}

#######変数を追加したら加える#####################
#\はコード上の改行。
company_info=[
company_n_emp_total,\
company_n_emp_m,\
company_n_emp_w,\
company_age_total,\
company_age_m,\
company_age_w,\
company_length_total,\
company_length_m,\
company_length_w,\
company_sal,\
company_new,\
company_mid,\
company_stay1_m,\
company_stay1_w,\
company_stay2,\
company_leave_m ]


start_year = 2014
end_year = 2019


#データの追加のための関数
def add_data(code,dic,year,data,year_id,data_id):
    try:
        try:
            dic[code]['20'+year[year_id]]=data[data_id].replace(',','')
        except TypeError:
            pass
                                               
    except KeyError:
        dic[code]={}
        try:
            dic[code]['20'+year[year_id]]=data[data_id].replace(',','')
        except TypeError:
            pass
        
#変数の辞書に対して欠損を補う処理を行う関数
def process_missing_data(val_dict):
    for data in val_dict.values():
        for i in range(start_year ,end_year+1):
            try:
                data[str(i)]==True #データが欠損でないときは何もしない
            except KeyError:
                data[str(i)]='ー'



files = glob.glob("./csr/*") #pdfファイル名の一覧を取得

for file in files[:5]: #filesの中からファイルを一個ずつ処理していく
    print(file)
    doc = fitz.open(file) #pdfの読み込み
    
    #複数ページを参照できるように変更しました。後半のtry-exceptラッシュは欲しい変数が書かれていないページを回しているとき(正規表現にマッチしないとき)にスキップするための部分です。。。
    for i in range(len(doc)):
        d = doc[i].getText()
        try:
            code = re.match(r'【.*】\n(\d*)\n',d)[1] #matchはテキストの先頭にマッチするかを判定する。codeは先頭にあるのでmatchにしました。
        except TypeError:
            pass
#####変数を増やすときに変更必要(3箇所,①re.searchから取ってくる部分　②上で定義した辞書に実際に値を入れるところ　③except KeyErrorの下の辞書の辞書を作る場所)##########################################
##########①re.searchから取ってくる部分######################       
        n_emp = re.search(r'(従業員数)（人）\t\n(\d*)年度\t\n([\d,―]+)\t\n([\d,―]+)\t\n([\d,―]+)\n\t\n(\d*)年度\t\n([\d,―]+)\t\n([\d,―]+)\t\n([\d,―]+)\n',d)
        length_of_service = re.search(r'(勤続年数)（年）\t\n(\d*)年度\t\n([\d,.―]+)\t\n([\d,.―]+)\t\n([\d,.―]+)\n\t\n(\d*)年度\t\n([\d,.―]+)\t\n([\d,.―]+)\t\n([\d,.―]+)\n',d)
        age = re.search(r'(平均年齢)（歳）\t\n(\d*)年度\t\n([\d,.―]+)\t\n([\d,.―]+)\t\n([\d,.―]+)\n\t\n(\d*)年度\t\n([\d,.―]+)\t\n([\d,.―]+)\t\n([\d,.―]+)\n',d)
        sal = re.search(r'(平均年間給与)（円）\t\n(\d*)年度\t\n([\d,―]+)\t\n(\d*)年度\t\n([\d,―]+)\n',d)
        new = re.search(r'【(新卒採用)】\t\n合計\t\n大卒計\t\n大卒男\t\n大卒女\t\n短・専門\t\n高卒・他\n(\d*)年4月入社\t\n([\d,.―]+)\t\n([\d,.―]+)\t\n([\d,.―]+)\t\n([\d,.―]+)\t\n([\d,.―]+)\t\n([\d,.―]+)\n(\d*)年4月入社\t\n([\d,.―]+)\t\n([\d,.―]+)\t\n([\d,.―]+)\t\n([\d,.―]+)\t\n([\d,.―]+)\t\n([\d,.―]+)\n',d)
        leave = re.search(r'【離職者数】\t\n合計\t\n早期\t\n自己\t\n会社\t\n転籍\t\n他\n男\t\n([\d,―]+)\t\n([\d,―]+)\t\n([\d,―]+)\t\n([\d,―]+)\t\n([\d,―]+)\t\n([\d,―]+)\n女\t\n([\d,―]+)\t\n([\d,―]+)\t\n([\d,―]+)\t\n([\d,―]+)\t\n([\d,―]+)\t\n([\d,―]+)\n男女計\t\n([\d,―]+)\t\n([\d,―]+)\t\n([\d,―]+)\t\n([\d,―]+)\t\n([\d,―]+)\t\n([\d,―]+)\n', d)
        #出力が上手くできてないファイルの確認用
        if code == '':
            print(file,'の出力が上手くいかない')
            
###########データの追加##########
#####後ろの数字二つは手探りで探さないといけないから少し面倒
        add_data(code,company_n_emp_total,n_emp,n_emp,6,7)
        add_data(code,company_n_emp_m,n_emp,n_emp,6,8)
        add_data(code,company_n_emp_w,n_emp,n_emp,6,9)
        add_data(code,company_length_total,length_of_service,length_of_service,6,7)
        add_data(code,company_length_m,length_of_service,length_of_service,6,8)
        add_data(code,company_length_w,length_of_service,length_of_service,6,9)
        add_data(code,company_age_total,age,age,6,7)
        add_data(code,company_age_m,age,age,6,8)
        add_data(code,company_age_w,age,age,6,9)
        add_data(code,company_sal,sal,sal,4,5)
        add_data(code,company_new,new,new,9,10)
        add_data(code,company_leave_m,sal,leave,4,1)

#####欠損データの処理       
for v_dict in company_info:
    process_missing_data(v_dict)


code_list = [key for key in company_n_emp_total ]

code_to_company = {}

#yahooファイナンスから証券コードに基づき会社名を取得
for code in code_list:
    text = requests.get( f'https://finance.yahoo.co.jp/quote/{code}.T')
    m = re.search(r' <title>(.*)【\d*】：詳細情報 - Yahoo!ファイナンス</title>', text.text)
    try:
        code_to_company[code]=m[1]
    except TypeError:
        code_to_company[code]='-' #会社名を取得できなかった場合(株式会社でない場合)
        print(code+"の会社名を取得に失敗")
    time.sleep(1)
    
    
#データの出力
print("データの出力")
with open('data_code_2.csv', mode='w', encoding='utf_8_sig') as f:

#変数を増やすときに変更必要#########################
    f.write('会社名,証券コード,従業員数-合計,勤続年数-合計,平均年齢-合計,平均年間給与,離職者数(男性),年度\n')

    for code in code_list:
        for i in range(start_year , end_year +1):
            i = str(i)
            
#変数を増やすときに変更必要#########################
            f.write(f'{code},{code_to_company[code]},{company_n_emp_total[code][i]},{company_length_total[code][i]},{company_age_total[code][i]},{company_sal[code][i]},{company_leave_m[code][i]},{i}\n')
print("出力完了")

