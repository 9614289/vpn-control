from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from ..callbacks import MenuCb
from ..keyboards import (
    kb_instruction_devices,
    kb_device_protocols,
    kb_proto_back,
)
from ..texts import instruction_intro_text, device_text, proto_text

router = Router()


@router.callback_query(MenuCb.filter(F.section == "instr"))
async def cb_instruction(call: CallbackQuery, callback_data: MenuCb):
    await call.message.edit_caption(
        caption=instruction_intro_text(),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb_instruction_devices(),
    )
    await call.answer()


@router.callback_query(MenuCb.filter(F.section == "device"))
async def cb_device(call: CallbackQuery, callback_data: MenuCb):
    device_code = callback_data.target or "unknown"

    await call.message.edit_caption(
        caption=device_text(device_code),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb_device_protocols(device_code),
    )
    await call.answer()


@router.callback_query(MenuCb.filter(F.section == "proto"))
async def cb_proto(call: CallbackQuery, callback_data: MenuCb):
    """
    Экран 'Инструкция → Устройство → Протокол'.
    Назад → в экран устройства (список протоколов).

    target в формате "device|proto" (важно: |, а не :).
    """
    if not callback_data.target or "|" not in callback_data.target:
        await call.answer("Некорректные данные", show_alert=True)
        return

    device_code, proto_code = callback_data.target.split("|", 1)

    await call.message.edit_caption(
        caption=proto_text(device_code, proto_code),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb_proto_back(device_code),
    )
    await call.answer()
