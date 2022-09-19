from bs4 import BeautifulSoup
import lxml
import requests
from fake_useragent import UserAgent
from db_actions import commit, add_product

def main_app():
    ua = UserAgent()
    print('User-Agent selected:',ua.random)
    headers = {'User-agent': ua.random}
    url = 'https://www.tabris.ru/pokupatelyam/aktsii/?CML2_TRAITS=Y&PAGEN_1=300'

    print('[[Страница акции загружается]]')
    result = requests.get(url, headers=headers)
    with open('index.html', 'w') as f:
        f.write(result.text)

    with open('index.html') as f:
        response = f.read()

    soup = BeautifulSoup(response, 'lxml')
    cards = soup.find_all('div', class_='widget-width ajax_class')
    products_count = 0

    for card in cards:
        print('[[Товар добавлен]]\n')
        card_url_customer = card.find('a', class_='tort-height').get('href')
        card_url = f'https://www.tabris.ru{card_url_customer}'

        try:
            card_sale = float(card.find('span', class_='card-item__sticker').text.strip().replace('- ','').replace('%', ''))
        except: continue

        card_product_name = card.find('span', class_= 'tort-order__title').text.strip()

        card_old_price = float(card.find('span', class_='tort-order__price tort-order__price-black').find('span', class_='tort-order-line').find('span').text.strip().replace(' руб.', '').replace(' ',''))

        card_new_price = int(float(card_old_price) * (100 - float(card_sale)) * 0.01)

        try:
            add_product(card_product_name, card_url, card_sale, card_old_price, card_new_price)
        except: continue
        products_count +=1
    print('[[Все товары обработаны успешно]]')

    commit()
    print('[[Сохранение в базе]]')
    return products_count, print('[[Все товары успешно загружены в базу]]')


if __name__=='__main__':
    main_app()