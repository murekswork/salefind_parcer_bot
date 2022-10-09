import os

from database import DatabaseActions
from parcer_lib import parse
from bot import bot
from app_logs import logger
from config import ADMIN_ID

db = DatabaseActions()


async def send_message_bot(product_list: list, user_id: int):
    """
    function takes product list from database and make decision about
    more effective way of send message to user that depends on message length
    :param product_list:
    :param user_id:
    :return:
    """
    if len(str(product_list)) >= 14000:
        file = open(f'{user_id}.txt', encoding='utf8', mode='a')
        for product in product_list:
            file.write(f'{product[0]} : {product[1]} : {product[2]} : {product[3]} : {product[4]}\n')
        file.close()
        await bot.send_document(user_id, open(f'{user_id}.txt', 'rb'))
        return os.remove(f'{user_id}.txt')

    message_text = ''
    for i, product in enumerate(product_list):
        if len(message_text) >= 3800:
            await bot.send_message(user_id, message_text)
            message_text = ''
        striped_name = product[0][:-20]
        message_text += f'{striped_name}\nСкидка{product[1]}\n' \
                        f'Ст. цена:{product[2]}\n' \
                        f'Цена:{product[3]}\n' \
                        f'www.tabris.ru{product[4]}\n\n'
    try:
        await bot.send_message(user_id, message_text)
    except:
        await bot.send_message(user_id, 'ниче не нашёл(')


async def find_by_name_controller(name: str, user_id: int):
    """
    function takes params name and int from handler, checks it and sends it to database function
    :param name:
    :param user_id:
    :return:
    """
    if name is None:
        return {'success': False, 'text': 'Ошибка! Пустое сообщение.'}
    search_product_result = db.find_by_name_db(name.lower())
    await send_message_bot(search_product_result, user_id)


async def parse_admin_func(user_id: int):
    """
    function takes user id for check if user is admin and then clears database and calls parcer function
    :param user_id:
    :return:
    """
    logger.debug('STARTED DATABASE REFRESHING')

    if user_id != ADMIN_ID:
        await bot.send_message(user_id, 'ты не админ бро)')
        logger.warning('NOT ADMIN USER TRIED TO REFRESH DATABASE')
        return False

    db.clear_database()

    logger.warning('PRODUCT TABLE WAS CLEARED')

    if parse()['success'] is True:
        logger.warning('DATABASE REFRESHED SUCCESSFULLY')
        await bot.send_message(user_id, 'Всё подргружено бро')
    else:
        logger.warning('COULDNT COMPLETE DATABASE REFRESH -> SEEMS LIKE PROBLEM WITH DB CONNECTION')
        await bot.send_message(user_id, 'Не смог подгрузить бро(')


async def find_by_sale_value_controller(sale_value: str, user_id):
    """
    function takes sale values and user id, then calls database function
    :param sale_value:
    :param user_id:
    :return:
    """
    if '-' in sale_value:
        sale_range = sale_value.split('-')
    elif ' ' in sale_value:
        sale_range = sale_value.split(' ')
    else:
        return await bot.send_message(user_id, 'не балуйся')

    db_result = db.find_by_sale_value_db(sale_range[0], sale_range[1])
    if len(db_result) <= 1:
        return await bot.send_message(user_id, 'ниче не смог найти (')
    await send_message_bot(db_result, user_id)


