from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from ..callbacks import MenuCb
from ..keyboards import kb_info_menu, kb_rules_back
from ..texts import info_text, rules_text

router = Router()


@router.callback_query(MenuCb.filter(F.section == "info"))
async def cb_info(call: CallbackQuery, callback_data: MenuCb):
    await call.message.edit_caption(
        caption=info_text(),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb_info_menu(),
    )
    await call.answer()


@router.callback_query(MenuCb.filter(F.section == "rules"))
async def cb_rules(call: CallbackQuery, callback_data: MenuCb):
    await call.message.edit_caption(
        caption=rules_text(),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb_rules_back(),
    )
    await call.answer()
