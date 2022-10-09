def run_bot():
    from aiogram import executor
    from bot import dp
    from app_logs import logger
    from handlers import menu_handlers
    logger.warning('BOT STARTED')
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    run_bot()