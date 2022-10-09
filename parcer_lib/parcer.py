import os

from bs4 import BeautifulSoup
import lxml
import requests
from fake_useragent import UserAgent
from app_logs import logger
from database import DatabaseActions

db = DatabaseActions()


class Parcer:
    """
        This class consists of params and methods which are provide parcer work
    """
    def __init__(self):
        self.product_count: int = 0
        self.user_agent: UserAgent = UserAgent().random
        self.headers: dict = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
                              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                                        'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

        self.url: str = 'https://www.tabris.ru/pokupatelyam/aktsii/?CML2_TRAITS=Y&PAGEN_1=300'
        self.url_data: str = self.get_url_data()

# get url data for parcing
    def get_url_data(self):
        response = requests.get(url=self.url, headers=self.headers)
        with open('response.txt', encoding='utf8', mode='w') as f:
            f.write(response.text)

        with open('response.txt', encoding='utf8', mode='r') as f:
            return f.read()

# set soup
    def get_soup(self):
        soup = BeautifulSoup(self.url_data, 'lxml')
        logger.warning('SET SOUP OBJECT')
        return soup

# adding card by card in database
    def get_cards(self, soup: BeautifulSoup):
        cards = soup.find_all('div', class_ = 'widget-width ajax_class')
        logger.warning('PARCER GOT ALL CARDS')
        for card in cards:
            card_url = card.find('a', class_='tort-height').get('href')
            try:
                card_sale = float(card.find('span', class_='card-item__sticker').text.strip().replace('- ', '').replace('%', ''))
            except:
                continue
            card_product_name = card.find('span', class_='tort-order__title').text.strip()

            card_old_price = float(card.find('span', class_='tort-order__price tort-order__price-black').
                                   find('span',class_='tort-order-line').
                                   find('span').
                                   text.
                                   strip().
                                   replace(' руб.', '').
                                   replace(' ', ''))

            card_new_price = int(float(card_old_price) * (100 - float(card_sale)) * 0.01)

            try:
                db.add_card_db(card_product_name, card_sale, card_old_price, card_new_price, card_url)
                self.product_count += 1
            except:
                continue

# commit after adding all cards
        print(self.product_count)
        logger.warning('PARCER END WORD')
        os.remove('response.txt')
        db.database_commit()

def parse():
    try:
        db.clear_database()
        app = Parcer()
        app.get_cards(soup=app.get_soup())
        logger.warning('SITE WAS SUCCESSFULLY PARSED!')
        return {'success': True}
    except Exception as ex:
        logger.warning(f'ERROR {ex}')
        return {'success': False, 'text': {ex}}
