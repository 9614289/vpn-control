from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from ..callbacks import MenuCb
from ..keyboards import kb_pay_menu
from ..texts import pay_text

router = Router()


@router.callback_query(MenuCb.filter(F.section == "pay"))
async def cb_pay(call: CallbackQuery, callback_data: MenuCb):
    if callback_data.action == "tariff":
        tariff_code = callback_data.target
        await call.answer(f"Заглушка: выбран {tariff_code}", show_alert=False)
        return

    await call.message.edit_caption(
        caption=pay_text(),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb_pay_menu(),
    )
    await call.answer()
