from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests


class Scraper:
    def __init__(self):
        self.url_for_requests = "http://www.osu.ru/pages/schedule/index.php"

    def get_filial(self):
        to_send = {
            'setfilial': ''
        }
        page = requests.post(self.url_for_requests, to_send)
        bsObj = BeautifulSoup(page.text, features="html.parser")
        a_parts = bsObj.find_all('a', {'class': 'btn', 'title': True})
        values = {}
        values_swapped = {}

        for i in a_parts:
            # print(i.attrs['href'][1:].split('=')[1])
            values[i.text] = int(i.attrs['href'][1:].split('=')[1])
            values_swapped[i.attrs['href'][1:].split('=')[1]] = i.text
        return values, values_swapped

    def get_faculty(self, filial: int):
        to_send = {
            'filial': filial
        }
        html = requests.post(self.url_for_requests, data=to_send)
        bsObj = BeautifulSoup(html.text, features="html.parser")
        div_pars = bsObj.find_all('option', {'value': True, 'title': True})
        values = {}
        values_swapped = {}
        for tag in div_pars:
            values.setdefault(tag.text, int(tag.attrs['value']))
            values_swapped.setdefault(tag.attrs['value'], tag.text)
        return values, values_swapped

    def get_courses(self, who: int, filial: int, faculty_id: int):
        to_send = {
            'who': who,
            'what': 1,
            'request': 'potok',  # group для группы, potok для курса
            'filial': filial,
            'mode': 'full',
            'facult': faculty_id
        }
        page = requests.post(self.url_for_requests, data=to_send)
        bsObj = BeautifulSoup(page.text, features="html.parser")
        values = bsObj.find_all('option', {'value': True, 'onclick': True, 'title': False})
        data = {}
        data_swapped = {}
        for value in values:
            data.setdefault(value.text, int(value.attrs['value']))
            data_swapped.setdefault(value.attrs['value'], value.text)
        return data, data_swapped

    def get_groups(self, who: int, filial: int, faculty_id: int, course_id: int):
        to_send = {
            'who': who,
            'what': 1,
            'request': 'group',
            'filial': filial,
            'mode': 'full',
            'facult': faculty_id,
            'potok': course_id
        }
        page = requests.post(self.url_for_requests, data=to_send)
        bsObj = BeautifulSoup(page.text, features='html.parser')
        values = bsObj.find_all('option', {'value': True, 'onclick': True, 'title': False})
        data = {}
        data_swapped = {}
        for value in values:
            if 'rasp' in value.attrs['onclick']:
                data.setdefault(value.text, int(value.attrs['value']))
                data_swapped.setdefault(value.attrs['value'], value.text)
        return data, data_swapped





# sc = Scraper()
# x, y = sc.get_groups(1, 1, 6543, 2018)
# print(x, y, sep='\n')
