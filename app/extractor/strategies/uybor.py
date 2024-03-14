from typing import List, Tuple, Generator
from functools import partial
import logging
import re

from . import BuildingExtractionStrategy
from ..viewmodels import BuildingViewModel

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class UyBorExtractionStrategy(BuildingExtractionStrategy):
    driver: webdriver.Chrome

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.headless = True

        self.driver = webdriver.Chrome(options=options)

    def extract(self) -> Generator[List[BuildingViewModel], None, None]:
        config = self._get_config()
        current_page = 1
        for sale_type, categories in config.items():
            for url_category in categories:
                url = url_category['url']
                category = url_category['category']
                self.driver.get(url)
                pagination_items = self.driver.find_elements(By.CSS_SELECTOR,
                                                             'ul.MuiPagination-ul.mui-style-nhb8h9 li a')
                max_page = int(pagination_items[-2].text)
                while current_page <= max_page:
                    wait = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.MuiGrid-root.MuiGrid-container'))
                    )
                    elements = self.driver.find_elements(By.CSS_SELECTOR,
                                                         'div.MuiGrid-root.MuiGrid-container '
                                                         'div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12'
                                                         '.MuiGrid-grid-sm-6.MuiGrid-grid-xl-12')
                    page_buildings: List[BuildingViewModel] = []
                    for element in elements:
                        territory = None
                        area = None
                        room = None
                        building_area = None
                        floor = None
                        price = None
                        floors_number = None
                        views_count = None
                        price_element = element.find_element(By.CSS_SELECTOR,
                                                             'div.MuiTypography-root.MuiTypography-h4.mui-style-1b9kwdl')
                        if price_element:
                            price = price_element.text
                            price = int(price.replace('у.е.', '').strip().replace(' ', ''))
                        rooms_element = element.find_element(By.CSS_SELECTOR,
                                                             'span.MuiTypography-root.MuiTypography-h6.mui-style-6q9hwm')
                        if rooms_element:
                            room = int(re.search(r'\d+', rooms_element.text).group())
                        building_area_and_floors_elements = element.find_elements(By.CSS_SELECTOR,
                                                                                  'div.MuiTypography-root.MuiTypography-body3.mui-style-14j8hnd')
                        building_area_element = building_area_and_floors_elements[0] if len(
                            building_area_and_floors_elements) > 0 else None
                        if building_area_element:
                            building_area = int(building_area_element.text.replace('м²', '').strip())
                        floors_element = building_area_and_floors_elements[1] if len(
                            building_area_and_floors_elements) > 1 else None
                        if floors_element:
                            floor, floors_number = floors_element.text.split('/')
                        territory_and_area_element = element.find_element(By.CSS_SELECTOR,
                                                                          'div.MuiTypography-root.MuiTypography-body3.mui-style-1kgu75x')
                        if territory_and_area_element:
                            splitted_territory = territory_and_area_element.text.split(', ')
                            territory = splitted_territory[0]
                            area = ', '.join(splitted_territory[1:])
                        phone_button_element = element.find_element(By.CSS_SELECTOR,
                                                                    'button[aria-label="show-phone-button"]')
                        phone_button_element.click()
                        user_phone = phone_button_element.text
                        user_name_element = element.find_element(By.CSS_SELECTOR, 'div.MuiStack-root.mui-style-wdnt3x')
                        user_name = user_name_element.find_element(By.CSS_SELECTOR,
                                                                   'div.MuiBox-root.mui-style-0 div.MuiTypography-root.MuiTypography-caption.mui-style-rzapeq').text
                        type_of_ad = user_name_element.find_element(By.CSS_SELECTOR,
                                                                    'span.MuiTypography-root.MuiTypography-caption.mui-style-1tdgzzf').text
                        element.find_element(By.CSS_SELECTOR, 'a.MuiBox-root.mui-style-1vssrzj').click()

                        self._switch_to_new_window()

                        views_elements = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                                 'div.MuiStack-root.MuiBox-root.mui-style-2b1uda div.MuiTypography-root.MuiTypography-body3.mui-style-1265kty'))
                        )
                        if len(views_elements) > 1:
                            views_element = views_elements[1]
                            views_count_text = views_element.find_element(By.TAG_NAME, 'strong').text
                            views_count = int(re.search(r'\d+', views_count_text).group())

                        building_repair_element = \
                        self.driver.find_elements(By.CSS_SELECTOR, 'div.MuiStack-root.mui-style-ekcp1r')[3]
                        building_repair = building_repair_element.find_element(By.CSS_SELECTOR,
                                                                               'div.MuiTypography-root.MuiTypography-body3.mui-style-xckitu').get_attribute(
                            "innerHTML")

                        self._close_window()
                        page_buildings.append(BuildingViewModel(
                            territory=territory,
                            area=area,
                            sell_type=sale_type,
                            room_number=room,
                            land_area=None,
                            building_area=building_area,
                            price=price,
                            floor=floor,
                            floor_number=floors_number,
                            building_repair=building_repair,
                            type_of_ad=type_of_ad,
                            source='uybor',
                            views=views_count,
                            user_name=user_name,
                            user_phone=user_phone
                        ))
                    yield page_buildings
                    current_page += 1
                    self._change_page(url, current_page)

    def _switch_to_new_window(self):
        parent = self.driver.current_window_handle
        windows = self.driver.window_handles
        for window in windows:
            if window != parent:
                self.driver.switch_to.window(window)

    def _close_window(self):
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[0])

    def _change_page(self, url: str, page: int):
        url += f'&page={page}'
        self.driver.get(url)

    @staticmethod
    def _get_config() -> dict:
        return {
            'sale': [
                {
                    'url': 'https://uybor.uz/listings?operationType__eq=sale&category__eq=7',
                    'category': 'Квартира'
                },
                {
                    'url': 'https://uybor.uz/listings?operationType__eq=sale&category__eq=8',
                    'category': 'Дом'
                },
                {
                    'url': 'https://uybor.uz/listings?operationType__eq=sale&category__eq=11',
                    'category': 'Земельный участок'
                },
                {
                    'url': 'https://uybor.uz/listings?operationType__eq=sale&category__eq=10',
                    'category': 'Для бизнеса'
                },
            ],
            'rent': [
                {
                    'url': 'https://uybor.uz/listings?operationType__eq=rent&category__eq=7',
                    'category': 'Квартира',
                },
                {
                    'url': 'https://uybor.uz/listings?operationType__eq=rent&category__eq=8',
                    'category': 'Дом',
                },
                {
                    'url': 'https://uybor.uz/listings?operationType__eq=rent&category__eq=10',
                    'category': 'Для бизнеса',
                },
            ]
        }
