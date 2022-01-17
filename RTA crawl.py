from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re

# Create a dataframe to store data

df = pd.DataFrame(columns=['name', 'mst', 'date', 'rep', 'address'])
'''
name: ten cong ty
mst: ma so thue
date: ngay hoat dong
rep (representative): nguoi dai dien
address: dia chi
'''

# Crawl
base_url = 'https://doanhnghiep.biz/'

url_list = ['{}?p={}'.format(base_url, str(page)) for page in range(1, 20)]

try:
    p = 1  # to track the pages

    for url in url_list:
        html_text = requests.get(url).text
        soup = bs(html_text, 'lxml')

        boxes = soup.find('div', class_='col-md-9')
        boxes = boxes.find_all('div')

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

        # if p == 1:
        #     df.to_csv('doanhnghiep_biz.csv', index=False)
        # else:
        #     df.to_csv('doanhnghiep_biz.csv', mode='a', index=False, header=False)

        print(p)
        p += 1

except:
    pass
