import bs4.element
from .abstract_scraper import AbstractScraper
from .scrap_mixin import ScraperMixin


class InfoScraper(AbstractScraper, ScraperMixin):
    def __init__(self, link: str):
        super().__init__(link)
        self._apartment_info_dict = {}
        self._currency = None
        self._city = None

    def _address_scraper(self, soup: bs4.element) -> None:
        """
        This method add in apartment info dict address and set the city
        :param soup: The beautifulsoup element from where you want to parse the address and city
        """
        if soup.find('div', attrs={'class': 'loc'}).find('a'):
            location = soup.find('div', attrs={'class': 'loc'}).find('a').text.split(', ')
            self._city = location[1] if len(location) > 1 else location[0]
            self._apartment_info_dict['address'] = location[0] if len(location) > 1 else None
            if '›' in self._city:  # for scrap yerevan from location like that Վայոց Ձոր › Եղեգնաձոր
                self._city = self._city.split('› ')[-1]
            if 'Երևան' in location[0]:  # for scrap yerevan from location like that Երևան › Քանաքեռ Զեյթուն
                self._city = 'Երևան'
                self._apartment_info_dict['address'] = location[0].split('› ')[-1]
        else:
            self._apartment_info_dict['address'] = None

    def _currency_scraper(self, soup: bs4.element) -> None:
        """
        This method add in apartment info dict price and set the currency
        :param soup: The beautifulsoup element from where you want to parse the currency and price
        """
        if soup.find('span', attrs={'class': 'price'}):
            price = soup.find('span', attrs={'class': 'price'}).text
            if '$' in price:
                self._apartment_info_dict['price'] = price.strip('$')
                self._currency = 'USD'
            elif '€' in price:
                self._apartment_info_dict['price'] = price.strip('€')
                self._currency = 'EURO'
            else:
                self._apartment_info_dict['price'] = price.strip('֏')
                self._currency = 'AMD'

    def _image_scraper(self, soup: bs4.element) -> None:
        """
        Method which add in apartment info dict image link
        :param soup: The beautifulsoup element from where you want to parse the image link
        """
        if soup.find('div', attrs={'class': 'p'}):
            self._apartment_info_dict['img'] = soup.find('div', attrs={'class': 'p'}).find('img')['src']
        else:
            self._apartment_info_dict['img'] = None

    def _footer_scraper(self, soup: bs4.element) -> None:
        """
        Method which add in apartment info dict id and update date
        :param soup: The beautifulsoup element from where you want to parse the add id and update(creation) date
        """
        self._apartment_info_dict['id'] = soup[0].text.split(':')[-1].strip()
        # check if add have update date(third element), take it else take creation date(second element)
        i = 2 if len(soup) > 2 else 1
        self._apartment_info_dict['update_date'] = soup[i].text.split(':', maxsplit=1 if i == 2 else -1)[-1].strip()

    def _table_scraper(self, soup: bs4.element) -> None:
        """
        Method which add in apartment info dict information from table in add
        :param soup: The beautifulsoup element from where you want to parse the apartment info
        """
        table_dict = {}
        if soup:
            for elem in soup:
                table_dict[elem.find('div', attrs={'class': 't'}).text] = elem.find('div', attrs={'class': 'i'}).text
            self._apartment_info_dict.update(self.change_keys(table_dict))

    def parse_link(self) -> tuple:
        """
        Method which call all scraper methods for ad and return info for database
        :return: A tuple like (apartment info dict, currency, city)
        """
        soup = self.soup()
        # separate add html page to 3 parts
        ref = soup.find('div', attrs={'class': 'vit'})
        footer = soup.find('div', attrs={'class': 'footer'}).find_all('span')
        info_table = soup.find('div', attrs={'id': 'attr'})

        self._address_scraper(ref)
        self._currency_scraper(ref)
        self._image_scraper(ref)
        self._footer_scraper(footer)
        self._table_scraper(info_table)
        return self.convert_values_type(self._apartment_info_dict), self._currency, self._city
