from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re


class Crawl:

    def __init__(self, base_url):
        self.base_url = base_url

    def crawl_href(self):
        # df = pd.DataFrame(columns=['status', 'phone', 'type'])
        # '''
        # status: Tình trạng
        # phone: Số điện thoại
        # type: Loại hình doanh nghiệp
        # '''

        html_text = requests.get(self.base_url).text
        soup = bs(html_text, 'html.parser')
        box = soup.find('div', class_='col-md-9')
        divs = box.find_all('div')

        href_ls = []

        for div in divs:
            href = div.find('a')['href'][1:]
            href_ls.append(href)

        return href_ls

    # def crawl_phone(self, com_url):



base_url = 'https://doanhnghiep.biz/'

scrape = Crawl(base_url)

# print(scrape.crawl_href())


