from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re

base_url = 'https://doanhnghiep.biz/'

html_text = requests.get(base_url).text
soup = bs(html_text, 'lxml')

boxes = soup.find('div', class_='col-md-9')
boxes = boxes.find_all('div')
df = pd.DataFrame(columns=['name', 'mst', 'date', 'rep', 'address'])
'''
name: ten cong ty
mst: ma so thue
date: ngay hoat dong
rep (representative): nguoi dai dien
address: dia chi
'''

for box in boxes:
    name = box.find('h6').find('a').string
    mst = box.find('a', title=re.compile('Tra cứu Số ĐKKD/MST.*')).string
    date = box.find(text=re.compile('Ngày hoạt động.*'))
    date = re.findall(r'\d{2}/\d{2}/\d{4}', date.string)[0]
    rep = box.find('em').find('a').string
    address = box.find('address')
    address = address.get_text()
    df = df.append({'name': name, 'mst': mst, 'date': date, 'rep': rep, 'address': address}, ignore_index=True)


print(df)

# df.to_csv('doanhnghiep_biz.csv', mode='a', index=False, header=False)




