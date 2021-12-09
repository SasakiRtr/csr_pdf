#!/usr/bin/env python
# coding: utf-8

import requests
import re
import edinet
import time
from pathlib import Path
from edinet.xbrl_file import XBRLFile

list_tosho1 = []


for page in range(1, 5):
    text = requests.get( f'http://www.jpubb.com/list/list.php?se=tou1&pageID={page}') #文字列formatでpageごとのurlを読み込む
    _m = re.findall(r"name'><a href='//.*'>(.*)</a></td>", text.text) #正規表現を用いて企業名を抽出
    m = [i.replace("\u3000", " ") for i in _m] 
    list_tosho1.extend(m)
    print(m)



#日付でfor文を回すための関数 https://qiita.com/ground0state/items/508e479335d82728ef91

from datetime import date, timedelta
def date_range(start, stop, step = timedelta(1)):
    current = start
    while current < stop:
        yield current
        current += step

reports = {}

for date in date_range(date(2019, 4, 1), date(2019, 4, 30)): #注意　一回流してからもう一回流すときdate_range関数を更新しないといけない
    print(date)
    documents = edinet.api.documents.get(date)
    for doc in documents.list:
        try:
            if re.match(r'有価証券報告書', doc.title):
                if doc.filer_name.replace("\u3000", " ") not in reports: #キーがない時は新たに企業名をキー,値がリストになるように追加
                    reports[doc.filer_name.replace("\u3000", " ")] = {str(date):doc.document_id}
                else: #すでにキーが存在するときは、リストの後ろに値を追加
                    reports[doc.filer_name.replace("\u3000", " ")][str(date)]=doc.document_id
        except TypeError:
            pass
        
tosho1_edinet = {}

for key, value in reports.items():
    _key = key.replace("株式会社","")
    if _key in list_tosho1:
        tosho1_edinet[key] = value


n_employee = {}

for company in tosho1_edinet:
    print(company)
    for year, doc in tosho1_edinet[company].items():
        xbrl_path = edinet.api.document.get_xbrl(doc, save_dir = Path.cwd())
        xbrl = XBRLFile(f"./{doc}_1.xbrl")
        try:
            n_e = re.search(r'<jpcrp_cor:NumberOfEmployees.*"CurrentYearInstant.*"[^>]*>(\d*)',str(xbrl._root)).group(1)
            n_employee[company] = {year:n_e}
        except AttributeError:
            print(f"Not found employee in {company}/{year}/{doc}")
            n_employee[company] = {year:None}




