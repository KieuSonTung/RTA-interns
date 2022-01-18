from bs4 import BeautifulSoup as bs
import requests
import pandas as pd


class Crawl:

    def __init__(self, base_url):
        self.base_url = base_url

    def crawl_all_pages(self):
        url_list = ['{}?p={}'.format(self.base_url, str(page)) for page in range(1, 30)]
        return url_list

    def crawl_href(self, url):

        html_text = requests.get(url).text
        soup = bs(html_text, 'html.parser')
        box = soup.find('div', class_='col-md-9')
        divs = box.find_all('div')

        href_ls = []

        for div in divs:
            href = div.find('a')['href'][1:]
            href_ls.append('{}{}'.format(self.base_url, href))

        return href_ls

    def crawl_data(self, href):
        # df = pd.DataFrame(columns=['name', 'inc_date', 'start_date', 'status', 'address',
        #                            'owner', 'taxid', 'phone', 'buss_cls'])
        output = pd.DataFrame()
        html_text = requests.get(href).text
        soup = bs(html_text, 'html.parser')

        data_itemprops = {
            'name': 'name',
            'inc_date': 'IncorporatedDate',
            'start_date': 'StartDate',
            'status': 'Status',
            'address': 'address',
            'taxid': 'taxID',
            'phone': 'Phone',
            'buss_cls': 'BusinessClass',
        }

        data_tags = {
            'name': 'th',
            'inc_date': 'td',
            'start_date': 'td',
            'status': 'td',
            'address': 'td',
            'taxid': 'td',
            'phone': 'td',
            'buss_cls': 'td',
        }

        com = {}

        fields = data_itemprops.keys()
        for field in fields:
            tag = data_tags.get(field)
            itemprop = data_itemprops.get(field)
            try:
                com[field] = soup.find(tag, itemprop=itemprop).string
            except:
                com[field] = None

        owner = soup.find('span', itemprop='Owner').find('a').string
        com['owner'] = owner

        output = output.append(com, ignore_index=True)
        return output



    def add_to_csv(self, p, output):
        if p == 1:
            output.to_csv('doanhnghiep_biz.csv', index=False)
        else:
            output.to_csv('doanhnghiep_biz.csv', mode='a', index=False, header=False)


url = 'https://doanhnghiep.biz/'

scrape = Crawl(base_url=url)

pages_url = scrape.crawl_all_pages()

p = 1

for page in pages_url:
    com_url = scrape.crawl_href(page)

    for href in com_url:
        output = scrape.crawl_data(href=href)
        scrape.add_to_csv(p, output)
        print(p)
        p += 1