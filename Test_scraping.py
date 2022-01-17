from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re
from Crawl_class import Crawl


base_url = 'https://doanhnghiep.biz/'

# create a dataframe to store data
df = pd.DataFrame(columns=['name', 'inc_date', 'start_date', 'status', 'address',
                           'owner', 'taxid', 'phone', 'buss_cls'])

'''
name: tên doanh nghiệp
inc_date (incorporated date): ngày cấp
start_date: ngay hoat dong
status: tinh trang
address: dia chi
onwer: nguoi dai dien
phone: so dien thoai
buss_cls (business class): loai hinh doanh nghiep
'''

scrape = Crawl(base_url)
href = scrape.crawl_href()
href_ls = ['{}{}'.format(base_url, h) for h in href]

p = 1

for h in href_ls:
    html_text = requests.get(h).text
    soup = bs(html_text, 'html.parser')

    name = soup.find('th', itemprop='name').string

    inc_date = soup.find('td', itemprop="IncorporatedDate").string

    start_date = soup.find('td', itemprop="StartDate").string

    status = soup.find('td', itemprop="Status").string

    address = soup.find('td', itemprop="address").string

    owner = soup.find('span', itemprop='Owner').find('a').string

    taxid = soup.find('td', itemprop='taxID').string

    phone = soup.find('td', itemprop='Phone').string
    phone = phone.replace(' ', '')

    buss_cls = soup.find('td', itemprop='BusinessClass').string

    com = {'name': name, 'inc_date': inc_date, 'start_date': start_date, 'status': status,
           'address': address, 'owner': owner, 'taxid': taxid, 'phone': phone,
           'buss_cls': buss_cls}

    df = df.append(com, ignore_index=True)

    print(com)

if p == 1:
    df.to_csv('doanhnghiep_biz2.csv', index=False)
else:
    df.to_csv('doanhnghiep_biz2.csv', mode='a', index=False, header=False)
