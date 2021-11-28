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

    def get_courses_chairs(self, who: int, filial: int, faculty_id: int):
        to_send = {
            'who': who,
            'what': 1,
            'request': 'potok' if who == 1 else 'kafedra',  # group для группы, potok для курса, prep для преподавателя
            'filial': filial,
            'mode': 'full',
            'facult': faculty_id
        }
        page = requests.post(self.url_for_requests, data=to_send)
        bsObj = BeautifulSoup(page.text, features="html.parser")
        data = {}
        data_swapped = {}
        if who == 1:
            values = bsObj.find_all('option', {'value': True, 'onclick': True, 'title': False})

            for value in values:
                data.setdefault(value.text, int(value.attrs['value']))
                data_swapped.setdefault(value.attrs['value'], value.text)
        else:
            values = bsObj.find_all('option', {'value': True, 'onclick': True, 'title': True})
            for value in values:
                if value.attrs['onclick'].count('prep') > 0 and who == 2:
                    data.setdefault(value.text, int(value.attrs['value']))
                    data_swapped.setdefault(value.attrs['value'], value.text)

        return data, data_swapped

    def get_groups_teachers(self, who: int, filial: int, faculty_id: int, course_id: int):
        to_send_student = {
            'who': who,
            'what': 1,
            'request': 'group',
            'filial': filial,
            'mode': 'full',
            'facult': faculty_id,
            'potok': course_id
        }
        to_send_teacher = {
            'who': who,
            'what': 1,
            'request': 'prep',
            'filial': filial,
            'mode': 'full',
            'facult': faculty_id,
            'kafedra': course_id
        }
        page = requests.post(self.url_for_requests, data=to_send_teacher if who == 2 else to_send_student)
        bsObj = BeautifulSoup(page.text, features='html.parser')
        data = {}
        data_swapped = {}
        if who == 1:
            values = bsObj.find_all('option', {'value': True, 'onclick': True, 'title': False})
            for value in values:
                if 'rasp' in value.attrs['onclick']:
                    data.setdefault(value.text, int(value.attrs['value']))
                    data_swapped.setdefault(value.attrs['value'], value.text)
        else:
            values = bsObj.find_all('option', {'value': True, 'onclick': True, 'title': True})
            for value in values:
                if value.attrs['onclick'].count('rasp') > 0 and who == 2:
                    data.setdefault(value.text, int(value.attrs['value']))
                    data_swapped.setdefault(value.attrs['value'], value.text)
        return data, data_swapped
