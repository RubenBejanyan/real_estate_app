from .abstract_scraper import AbstractScraper
from constants import BASE_URL, CATEGORY_LINK


class LinkScraper(AbstractScraper):
    def __init__(self, link: str = CATEGORY_LINK):
        super().__init__(link)

    def link_generator(self) -> str:
        """
        This method generates links for individual ads from a category
        :return: individual ad link
        """
        soup = self.soup()
        divs = soup.find_all('div', attrs={"class": "dl"})
        a_tags = divs[0].find_all('a') + divs[1].find_all('a') if len(divs) > 1 else divs.find_all('a')
        for tag in a_tags:
            if "category" not in tag["href"] and "Փնտրում եմ" not in tag.text:
                yield f"{BASE_URL}{tag['href']}"
