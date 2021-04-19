import requests
import os
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"

# categories = {
#     "60": "bn",  # bnakaranner -> index = bn
#     "62": "tn",  # tner -> index = tn
#     "55": "hogh",  # hoghataracq -> index = hogh
#     "199": "kom",  # komercion -> index = kom
#     "173": "avto"  # avtotnakner & kayanateghi -> index = avto
# }


class LinkScraper:
    def __init__(self, link_list_file=None, category_url="https://www.list.am/category/60"):
        self.base_url = "https://www.list.am"
        self.category_url = category_url
        self.link_list_file = link_list_file

    def create_link_list(self):
        response = requests.get(self.category_url, headers={'User-Agent': USER_AGENT})
        data = response.content
        soup = BeautifulSoup(data, 'lxml')
        divs = soup.find_all('div', attrs={"class": "dl"})
        a_tags = divs[0].find_all('a') + divs[1].find_all('a')
        dir_path = os.path.join('.', 'Links')
        os.makedirs(dir_path, exist_ok=True)  # create ./Links directory, if it already exist, do nothing
        self.link_list_file = os.path.join(dir_path, "link_list.txt")
        with open(self.link_list_file, 'a+') as link_list:
            for tag in a_tags:
                if "category" not in tag["href"] and "Փնտրում եմ" not in tag.text:
                    if not self.already_in_link_list(f"{self.base_url}{tag['href']}\n"):
                        link_list.write(f"{self.base_url}{tag['href']}\n")

    def link_generator(self):
        with open(self.link_list_file, 'r') as link_list:
            for _link in link_list:
                yield _link[:-1]

    def already_in_link_list(self, link_to_check):
        with open(self.link_list_file, 'r+') as link_list:
            return link_to_check in link_list.readlines()


if __name__ == '__main__':
    ls = LinkScraper(link_list_file=os.path.join('.', 'Links', 'link_list.txt'))
    ls.create_link_list()
    for link in ls.link_generator():
        print(link)
