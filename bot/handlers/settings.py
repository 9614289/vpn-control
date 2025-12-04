from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from ..callbacks import MenuCb
from ..keyboards import kb_settings_menu
from ..texts import settings_text

router = Router()


@router.callback_query(MenuCb.filter(F.section == "settings"))
async def cb_settings(call: CallbackQuery, callback_data: MenuCb):
    await call.message.edit_caption(
        caption=settings_text(),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb_settings_menu(),
    )
    await call.answer()
