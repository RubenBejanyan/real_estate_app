from .info_scraper import InfoScraper
from .link_scraper import LinkScraper


def scraping() -> tuple:
    """
    Function which generate info for db for every individual ad in category
    :return: A tuple like (apartment info dict, currency, city)
    """
    l_s = LinkScraper()
    for _link in l_s.link_generator():
        i_s = InfoScraper(_link)
        yield i_s.parse_link()
