from constants import DICT_ARM_ENG
from datetime import datetime
from googletrans import Translator
from re import match


class ScraperMixin:
    @staticmethod
    def change_keys(dictionary: dict) -> dict:
        return {DICT_ARM_ENG[k]: v for k, v in dictionary.items()}

    @staticmethod
    def change_to_bool(text: str) -> bool:
        return text in {'Այո', 'Առկա է'}

    @staticmethod
    def change_to_int(text: str) -> int:
        a = text.split()
        # need to check it because price in ad wrote like 46,000 $
        if ',' in a[0]:
            a[0] = a[0].replace(',', '')
        return int(a[0])

    @staticmethod
    def change_to_float(text: str) -> float:
        a = text.split()
        if ',' in a[0]:
            a[0] = a[0].replace(',', '.')
        return float(a[0])

    @staticmethod
    def change_to_datetime(date_str_hy: str) -> datetime:
        """
        Can be two types of update date: first like 20.07.2021 if ad have only creation date,
                                         second like Մայիս 01, 2021 16:33
        In second case we need at first translate month
        :param date_str_hy: date in armenian
        :return: update date datetime object
        """
        if match('^[0-9.]+$', date_str_hy):
            return datetime.strptime(date_str_hy, '%d.%m.%Y')
        date_str_en = Translator().translate(date_str_hy, src='hy').text
        return datetime.strptime(date_str_en, '%B %d, %Y %H:%M')

    @staticmethod
    def convert_values_type(info_dict: dict) -> dict:
        """
        Method which convert dict values type from string to what we need
        :param info_dict: info dict with values type str
        :return: info dict with converted values types
        """
        info_dict['id'] = ScraperMixin.change_to_int(info_dict['id'])
        info_dict['update_date'] = ScraperMixin.change_to_datetime(info_dict['update_date'])

        if 'price' in info_dict.keys():
            info_dict['price'] = ScraperMixin.change_to_int(info_dict['price'])
        else:
            info_dict['price'] = None

        if 'new_building' in info_dict.keys():
            info_dict['new_building'] = ScraperMixin.change_to_bool(info_dict['new_building'])
        else:
            info_dict['new_building'] = None

        if 'elevator' in info_dict.keys():
            info_dict['elevator'] = ScraperMixin.change_to_bool(info_dict['elevator'])
        else:
            info_dict['elevator'] = None

        if 'floor' in info_dict.keys():
            floor = info_dict['floor'].split(' / ')
            info_dict['floor'] = ScraperMixin.change_to_int(floor[0])
            info_dict['max_floor'] = ScraperMixin.change_to_int(floor[1])
        else:
            info_dict['floor'] = None

        if 'rooms' in info_dict.keys():
            info_dict['rooms'] = ScraperMixin.change_to_int(info_dict['rooms'].strip('+'))
        else:
            info_dict['rooms'] = None

        if 'restrooms' in info_dict.keys():
            info_dict['restrooms'] = ScraperMixin.change_to_int(info_dict['restrooms'].strip('+'))
        else:
            info_dict['restrooms'] = None

        if 'area' in info_dict.keys():
            info_dict['area'] = ScraperMixin.change_to_float(info_dict['area'])
        else:
            info_dict['area'] = None

        if 'ceiling_height' in info_dict.keys():
            info_dict['ceiling_height'] = ScraperMixin.change_to_float(info_dict['ceiling_height'])
        else:
            info_dict['ceiling_height'] = None

        return info_dict
