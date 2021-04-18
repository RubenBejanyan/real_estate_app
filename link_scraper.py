import requests
import os
from bs4 import BeautifulSoup
# from pprint import pprint
import lxml

# real estate Categories
categories = {
    "60": "bn",  # bnakaranner -> index = bn
    "62": "tn",  # tner -> index = tn
    "55": "hogh",  # hoghataracq -> index = hogh
    "199": "kom",  # komercion -> index = kom
    "173": "avto"  # avtotnakner & kayanateghi -> index = avto
}

BASE_URL = "https://www.list.am/category/"
PAGE_URL = "https://www.list.am"

category_links = []
category_dict = dict()

for i in categories:
    category_links.append(f"{BASE_URL}{i}")

for link in category_links:
    key = os.path.basename(link)
    response = requests.get(link, headers={
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"
    })
    if response.status_code == 200:
        with open(fr".\Categories\Listam_category_{categories[key]}.html", "wb+") as file:
            file.write(response.content)
    else:
        print(response.text)

    with open(fr".\Categories\Listam_category_{categories[key]}.html", "rb+") as html_file:
        data = html_file.read()

    soup = BeautifulSoup(data, 'lxml')
    divs = soup.find_all('div', attrs={"class": "dl"})
    a_tags = divs[0].find_all('a') + divs[1].find_all('a')

    with open(fr".\Links\Listam_category_{categories[key]}.txt", 'a') as info_txt:
        for tag in a_tags:
            if "category" not in tag["href"]:
                info_txt.write(f"{PAGE_URL}{tag['href']}\n")


def link_reader(FILE_PATH):
    with open(FILE_PATH, 'r') as link_file:
        for link_ in file:
            yield link_[:-1]


