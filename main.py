from __future__ import annotations

from dotenv import load_dotenv

load_dotenv()

import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import BotConfig
from router import create_router
from services import PromoAPIClient

logger = logging.getLogger(__name__)

async def run_bot() -> None:
    logging.basicConfig(level=logging.DEBUG)
    config = BotConfig.from_env()
    api_client = PromoAPIClient(config.api_base_url)
    bot = Bot(token=config.token)
    dp = Dispatcher()
    dp.include_router(create_router(config, api_client))

    try:
        logger.info("Bot is starting. Web App URL: %s", config.web_app_url)
        await dp.start_polling(bot)
    finally:
        await api_client.close()


def main() -> None:
    asyncio.run(run_bot())


if __name__ == "__main__":
    main()
