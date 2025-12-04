from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from ..callbacks import MenuCb
from ..keyboards import kb_ref_menu, kb_exchange_menu
from ..texts import ref_text, exchange_text

router = Router()


@router.callback_query(MenuCb.filter(F.section == "ref"))
async def cb_ref(call: CallbackQuery, callback_data: MenuCb):
    await call.message.edit_caption(
        caption=ref_text(call.from_user.id),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb_ref_menu(),
    )
    await call.answer()


@router.callback_query(MenuCb.filter(F.section == "exch"))
async def cb_exchange(call: CallbackQuery, callback_data: MenuCb):
    await call.message.edit_caption(
        caption=exchange_text(),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb_exchange_menu(),
    )
    await call.answer()
