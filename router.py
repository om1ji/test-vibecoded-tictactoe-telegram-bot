import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, WebAppInfo

from config import BotConfig
from services import PromoAPIClient, PromoAPIError
from utils import build_web_app_url

logger = logging.getLogger(__name__)


def format_history(promos: list[dict]) -> str:
    if not promos:
        return (
            "<b>Побед пока нет</b>\n"
            "Откройте мини-приложение, выиграйте партию — и первый промокод появится здесь ✨"
        )

    lines = ["<b>Ваши промокоды</b>"]
    for idx, item in enumerate(promos, start=1):
        code = item.get("code", "????")
        lines.append(f"<b>{idx}.</b> <code>{code}</code>")
    return "\n".join(lines)


def create_router(config: BotConfig, promo_api: PromoAPIClient) -> Router:
    router = Router()

    @router.message(CommandStart())
    async def cmd_start(message: Message) -> None:
        user = message.from_user
        if not user:
            await message.answer("Не удалось определить пользователя Telegram.")
            return

        await message.answer(
            "<b>Привет!</b>\n"
            "Я сопровождаю ваше путешествие в мини-игре <i>TicTacToe</i>."
            "Нажмите кнопку <b>Играть</b> — она откроет крестики-нолики."
            "В любой момент используйте /help, чтобы узнать команды.",
            parse_mode="HTML"
        )

    @router.message(Command("help"))
    async def cmd_help(message: Message) -> None:
        await message.answer(
            "<b>Команды бота</b>\n"
            "/start — показать кнопку запуска мини-приложения.\n"
            "/promos — список последних промокодов.\n"
            "/help — краткая справка.\n\n"
            "После каждой победы мини-приложение покажет промокод внутри себя, "
            "а мы в боте сохраним историю для вашего удобства.",
            parse_mode="HTML"
        )

    @router.message(Command("promos"))
    async def cmd_promos(message: Message) -> None:
        user = message.from_user
        if not user:
            await message.answer("Не удалось определить пользователя Telegram.")
            return
        try:
            promos = await promo_api.promo_history(user.id)
        except PromoAPIError:
            await message.answer("Не получилось связаться с Promo API. Попробуйте позже.")
            return

        history_text = format_history(promos)
        await message.answer(history_text, parse_mode="HTML")

    return router
