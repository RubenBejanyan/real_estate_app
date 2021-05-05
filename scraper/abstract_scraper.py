import requests
from bs4 import BeautifulSoup
from constants import USER_AGENT


class AbstractScraper:
    def __init__(self, link: str):
        self.link = link

    def soup(self) -> BeautifulSoup:
        """
        Method which check response status and return bs
        :return: BeautifulSoup from the self.link
        :raise Exception: if response status code not 200
        """
        response = requests.get(self.link, headers={'User-Agent': USER_AGENT})
        if response.status_code == 200:
            return BeautifulSoup(response.content, 'lxml')
        else:
            raise Exception(f'{response.status_code} ::: {response.text}')
