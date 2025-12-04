import logging

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from ..config import MAIN_MENU_PHOTO_ID
from ..keyboards import kb_main_menu
from ..texts import main_menu_caption
from ..callbacks import MenuCb

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer_photo(
        MAIN_MENU_PHOTO_ID,
        caption=main_menu_caption(message.from_user.id),
        reply_markup=kb_main_menu(),
    )


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer_photo(
        MAIN_MENU_PHOTO_ID,
        caption=main_menu_caption(message.from_user.id),
        reply_markup=kb_main_menu(),
    )


@router.callback_query(MenuCb.filter(lambda c: c.section == "main"))
async def cb_main_menu(call, callback_data: MenuCb):
    try:
        await call.message.delete()
    except Exception:
        pass

    await call.message.answer_photo(
        MAIN_MENU_PHOTO_ID,
        caption=main_menu_caption(call.from_user.id),
        reply_markup=kb_main_menu(),
    )
    await call.answer()
