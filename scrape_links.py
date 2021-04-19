
import requests
from bs4 import BeautifulSoup
import os
current = os.getcwd()



class scraper:

    def __init__(self,links_file):
        self.links_file = links_file
        self.files_name = []

    def top(self):
        self.url_request()
        output_list = []
        for el in self.files_name:
            output_list.append(self.parse_file(el))
        return output_list


    def save_html_files(self, endpoint,file_name):
        response = requests.get(endpoint, headers={
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"
        })

        if response.status_code == 200:
            with open(file_name, 'w+b') as html_file:
                html_file.write(response.content)
                self.files_name.append(file_name)
        else:
            print(response.status_code)
            print(response.text)

    def url_request(self):
        file_num = 11
        link_list =  open(self.links_file, 'r+').readlines()
        for link in link_list:
            self.save_html_files(link,f'link{file_num}.html')
            file_num +=1


    def parse_file(self,file_name):
        with open (file_name,encoding='utf8') as f:
            text =f.read()

        soup =BeautifulSoup(text, 'html.parser')
        ref = soup.find('div', attrs={'class': 'vit'})
        footer = soup.find('div', attrs={'class': 'footer'}).find_all('span')

        info_dict = {'title' : ref.find('h1').text,
                     'img': ref.find('div',attrs={'class' : 'p'}).find('img')['src'],
                     'loaction': ref.find('div',attrs={'class' : 'loc'}).find('a').text,
                     'body': soup.find('div', attrs={'class': 'body'}).text,
                     footer[0].text.split(':')[0].strip() : footer[0].text.split(':')[-1].strip(),
                     footer[1].text.split(':')[0].strip() : footer[1].text.split(':')[-1].strip(),
                     }

        # There are some cases where clabel is missing
        if (ref.find('span',attrs={'class' : 'clabel'})):
            info_dict['clabel'] = ref.find('span',attrs={'class' : 'clabel'}).text

        #checks if announcement updated
        if(len(footer)>2):
            info_dict[footer[2].text.split(':',1)[0].strip()] : footer[2].text.split(':',1)[-1].strip()

        #checks if price exists
        if(ref.find('span',attrs={'class' : 'price'})):
            info_dict['price'] = ref.find('span',attrs={'class' : 'price'}).text


        #scrapes the midle part(like a table) of annaouncement
        item_info = soup.find('div', attrs={'id': 'attr'})

        for el in item_info:
         info_dict[el.find('div',attrs = {'class':'t'}).text] = el.find('div',attrs = {'class':'i'}).text

        return info_dict


if __name__ == '__main__':
    a= scraper('links.txt')
    result = a.top()
    for link_info in result:
        for el in link_info:
            print(el,(25-len(el))*" ",link_info[el])
        print('**********************************************************************************')
