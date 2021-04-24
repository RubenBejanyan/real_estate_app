import requests
from bs4 import BeautifulSoup
from datetime import datetime


class AbstractScraper:
    def __init__(self, link):
        self.link = link
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"

    def soup(self):
        response = requests.get(self.link, headers={'User-Agent': self.user_agent})
        if response.status_code == 200:
            return BeautifulSoup(response.content, 'lxml')
        else:
            print(response.status_code)
            print(response.text)


class LinkScraper(AbstractScraper):
    def __init__(self, link="https://www.list.am/category/60"):
        super().__init__(link)
        self.base_url = "https://www.list.am"

    def link_generator(self):
        soup = self.soup()
        divs = soup.find_all('div', attrs={"class": "dl"})
        a_tags = divs[0].find_all('a') + divs[1].find_all('a') if len(divs) > 1 else divs.find_all('a')
        for tag in a_tags:
            if "category" not in tag["href"] and "Փնտրում եմ" not in tag.text:
                yield f"{self.base_url}{tag['href']}"


class InfoScraper(AbstractScraper):
    def __init__(self, link):
        super().__init__(link)

    def parse_file(self):
        soup = self.soup()
        ref = soup.find('div', attrs={'class': 'vit'})
        footer = soup.find('div', attrs={'class': 'footer'}).find_all('span')
        currency = None
        city = None
        apartment_info_dict = {'id': footer[0].text.split(':')[-1].strip(),
                               'update_date': footer[1].text.split(':')[-1].strip()}
        if len(footer) > 2:  # check if add have update date, change creation date to update date
            apartment_info_dict['update_date'] = footer[2].text.split(':', 1)[-1].strip()
        # checks if picture exist
        if ref.find('div', attrs={'class': 'p'}):
            apartment_info_dict['img'] = ref.find('div', attrs={'class': 'p'}).find('img')['src']
        if ref.find('div', attrs={'class': 'loc'}).find('a'):
            location = ref.find('div', attrs={'class': 'loc'}).find('a').text.split(', ')
            print(location)
            city = location[1] if len(location) > 1 else location[0]
            apartment_info_dict['address'] = location[0] if len(location) > 1 else None
            if '›' in city:  # for scrap yerevan from location like that Վայոց Ձոր › Եղեգնաձոր
                city = city.split('› ')[-1]
            if 'Երևան' in location[0]:  # for scrap yerevan from location like that Երևան › Քանաքեռ Զեյթուն
                city = 'Երևան'
                apartment_info_dict['address'] = location[0].split('› ')[-1]
        # checks if price exists
        if ref.find('span', attrs={'class': 'price'}):
            price = ref.find('span', attrs={'class': 'price'}).text
            if '$' in price:
                apartment_info_dict['price'] = price.split('$')[-1]
                currency = 'USD'
            else:
                apartment_info_dict['price'] = price.split('֏')[0]
                currency = 'AMD'
        # scrapes the middle part(like a table) of announcement
        item_info = soup.find('div', attrs={'id': 'attr'})
        table_dict = {}
        if item_info:
            for elem in item_info:
                table_dict[elem.find('div', attrs={'class': 't'}).text] = elem.find('div', attrs={'class': 'i'}).text
            apartment_info_dict.update(self.change_keys(table_dict))  # change keys to english and update info dict
        return apartment_info_dict, currency, city

    @staticmethod
    def change_keys(dictionary):
        english_keys = ['building_type', 'new_building', 'elevator', 'floor', 'rooms', 'restrooms', 'area',
                        'ceiling_height', 'balcony', 'renovation']
        arm_keys = ['Շինության տիպը', 'Նորակառույց', 'Վերելակ', 'Հարկ', 'Սենյակների քանակ', 'Սանհանգույցների քանակ',
                    'Ընդհանուր մակերեսը', 'Առաստաղի բարձրությունը', 'Պատշգամբ', 'Վերանորոգում']
        dict_arm_eng = dict(zip(arm_keys, english_keys))
        new_dict = {dict_arm_eng[k]: v for k, v in dictionary.items()}
        return new_dict


if __name__ == '__main__':
    start = datetime.now()
    l_s = LinkScraper()
    for index, _link in enumerate(l_s.link_generator()):
        i_s = InfoScraper(_link)
        data, currency, city = i_s.parse_file()
        print(data, currency, city, sep='\n')
        print('=============')
    print(datetime.now() - start)
