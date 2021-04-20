
import requests
from bs4 import BeautifulSoup
import os
import lxml
import json

current = os.getcwd()



class scraper:

    def __init__(self, links_file):
        self.links_file = links_file
        self.output_list = []
        self.status = 0

    def scrape(self):
        self.url_request()
        return self.output_list

    def save_html_files (self, endpoint, file_name):
        response = requests.get(endpoint, headers={
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"
        })
        if response.status_code == 200:
            self.status = 0
            with open(file_name, 'wb+') as html_file:
                html_file.write(response.content)
        else:
            self.status = 1
            print(response.status_code,'Error | skipping this one --> ', file_name)

    def url_request(self):
        file_num = 1
        link_list = open(self.links_file, 'r+').readlines()
        for link in link_list:
            self.save_html_files(link,f'link{file_num}.html')
            if not self.status:
                self.output_list.append(self.parse_file(f'link{file_num}.html'))
            file_num += 1

    def parse_file(self, file_name):
        with open(file_name, 'rb+') as f:
            text = f.read()

        soup = BeautifulSoup(text, 'lxml')
        ref = soup.find('div', attrs={'class': 'vit'})
        footer = soup.find('div', attrs={'class': 'footer'}).find_all('span')

        info_dict = {'title': ref.find('h1').text,
                     'location': ref.find('div',attrs={'class': 'loc'}).find('a').text,
                     'body': soup.find('div', attrs={'class': 'body'}).text,
                     footer[0].text.split(':')[0].strip(): footer[0].text.split(':')[-1].strip(),
                     footer[1].text.split(':')[0].strip(): footer[1].text.split(':')[-1].strip(),
                     }

        if ref.find('div',attrs={'class': 'p'}):
            info_dict['img'] = ref.find('div', attrs={'class': 'p'}).find('img')['src']

        # checks if clabel is setted
        if ref.find('span',attrs={'class' : 'clabel'}):
            info_dict['clabel'] = ref.find('span', attrs={'class': 'clabel'}).text

        #checks if announcement updated
        if len(footer)>2:
            info_dict[footer[2].text.split(':', 1)[0].strip()]: footer[2].text.split(':', 1)[-1].strip()

        #checks if price exists
        if ref.find('span',attrs={'class': 'price'}):
            price = ref.find('span', attrs={'class': 'price'}).text
            if '$' in price :
                info_dict['currency'] = 'USD'
                info_dict['price'] = price.split('$')[-1]
            else:
                info_dict['currency'] = 'AMD'
                info_dict['price'] = price.split('֏')[0]


        #scrapes the midle part(like a table) of annaouncement
        item_info = soup.find('div', attrs={'id': 'attr'})

        for el in item_info:
            info_dict[el.find('div', attrs={'class': 't'}).text] = el.find('div',attrs={'class': 'i'}).text

        return info_dict


if __name__ == '__main__':
    a = scraper('links.txt')
    result = a.scrape()
    result2 = (json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False))
    with open('results.txt', 'w+', encoding='utf-8')as f:
        f.write(result2)

#    for link_info in result:
#        for el in link_info:
#            print(el, (25-len(el))*" ", link_info[el])
#        print('**********************************************************************************')
