import requests
from bs4 import BeautifulSoup
import os
from link_scraper import LinkScraper

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"


class InfoScraper:
    def __init__(self, link):
        self.link = link
        self.file_name = None

    def save_html_file(self):
        response = requests.get(self.link, headers={'User-Agent': USER_AGENT})
        if response.status_code == 200:
            dir_path = os.path.join('.', 'html_files')
            os.makedirs(dir_path, exist_ok=True)
            self.file_name = os.path.join(dir_path, str(self.link).split('/')[-1])
            with open(self.file_name, 'wb+') as html_file:
                html_file.write(response.content)
        else:
            print(response.status_code)
            print(response.text)

    def parse_file(self):
        with open(self.file_name, encoding='utf8') as f:
            text = f.read()

        soup = BeautifulSoup(text, 'html.parser')
        ref = soup.find('div', attrs={'class': 'vit'})
        footer = soup.find('div', attrs={'class': 'footer'}).find_all('span')

        info_dict = {footer[0].text.split(':')[0].strip(): footer[0].text.split(':')[-1].strip(),
                     footer[1].text.split(':')[0].strip(): footer[1].text.split(':')[-1].strip(),
                     'location': ref.find('div', attrs={'class': 'loc'}).find('a').text,
                     }

        # checks if announcement updated
        if len(footer) > 2:
            info_dict[footer[2].text.split(':', 1)[0].strip()]: footer[2].text.split(':', 1)[-1].strip()

        # checks if price exists
        if ref.find('span', attrs={'class': 'price'}):
            info_dict['price'] = ref.find('span', attrs={'class': 'price'}).text

        # checks if picture exist
        if ref.find('div', attrs={'class': 'p'}):
            info_dict['img'] = ref.find('div', attrs={'class': 'p'}).find('img')['src']

        # scrapes the middle part(like a table) of announcement
        item_info = soup.find('div', attrs={'id': 'attr'})

        # TODO
        if item_info:
            for elem in item_info:
                info_dict[elem.find('div', attrs={'class': 't'}).text] = elem.find('div', attrs={'class': 'i'}).text

        return info_dict


if __name__ == '__main__':
    l_s = LinkScraper()
    l_s.create_link_list()
    for index, _link in enumerate(l_s.link_generator()):
        i_s = InfoScraper(_link)
        i_s.save_html_file()
        print(index, i_s.parse_file())
