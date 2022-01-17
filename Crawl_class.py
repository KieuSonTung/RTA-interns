from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re


class Crawl:

    def __init__(self, base_url):
        self.base_url = base_url

    def crawl_href(self):

        html_text = requests.get(self.base_url).text
        soup = bs(html_text, 'html.parser')
        box = soup.find('div', class_='col-md-9')
        divs = box.find_all('div')

        href_ls = []

        for div in divs:
            href = div.find('a')['href'][1:]
            href_ls.append('{}{}'.format(base_url, href))

        return href_ls

    def crawl_data(self, h):
        df = pd.DataFrame(columns=['name', 'inc_date', 'start_date', 'status', 'address',
                                   'owner', 'taxid', 'phone', 'buss_cls'])

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

        df.append(com, ignore_index=True)

        return df

    def add_to_csv(self, p):
        if p == 1:
            self.df.to_csv('doanhnghiep_biz.csv', index=False)
        else:
            self.df.to_csv('doanhnghiep_biz.csv', mode='a', index=False, header=False)


base_url = 'https://doanhnghiep.biz/'

scrape = Crawl(base_url)

com_url = scrape.crawl_href()

p = 1

print(scrape.crawl_data(com_url[0]))

