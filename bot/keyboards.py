from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callbacks import MenuCb
from .texts import DEVICES, PROTOCOLS, TARIFFS


def kb_main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 Оплата",
                    callback_data=MenuCb(section="pay", action="open").pack(),
                ),
                InlineKeyboardButton(
                    text="ℹ️ Информация",
                    callback_data=MenuCb(section="info", action="open").pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="👥 Реферальная программа",
                    callback_data=MenuCb(section="ref", action="open").pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⚙️ Настройки",
                    callback_data=MenuCb(section="settings", action="open").pack(),
                )
            ],
        ]
    )


def kb_pay_menu() -> InlineKeyboardMarkup:
    buttons_row1 = [
        InlineKeyboardButton(
            text=title,
            callback_data=MenuCb(section="pay", action="tariff", target=code).pack(),
        )
        for code, title in TARIFFS[:2]
    ]
    buttons_row2: list[InlineKeyboardButton] = []
    if len(TARIFFS) > 2:
        code, title = TARIFFS[2]
        buttons_row2.append(
            InlineKeyboardButton(
                text=title,
                callback_data=MenuCb(
                    section="pay", action="tariff", target=code
                ).pack(),
            )
        )

    kb: list[list[InlineKeyboardButton]] = [buttons_row1]
    if buttons_row2:
        kb.append(buttons_row2)

    kb.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=MenuCb(section="main", action="open").pack(),
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=kb)


def kb_info_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📘 Инструкция",
                    callback_data=MenuCb(section="instr", action="open").pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📜 Правила",
                    callback_data=MenuCb(section="rules", action="open").pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=MenuCb(section="main", action="open").pack(),
                )
            ],
        ]
    )


def kb_instruction_devices() -> InlineKeyboardMarkup:
    kb_rows: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []

    for code, title in DEVICES:
        row.append(
            InlineKeyboardButton(
                text=title,
                callback_data=MenuCb(
                    section="device", action="open", target=code
                ).pack(),
            )
        )
        if len(row) == 2:
            kb_rows.append(row)
            row = []
    if row:
        kb_rows.append(row)

    kb_rows.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=MenuCb(section="info", action="open").pack(),
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=kb_rows)


def kb_device_protocols(device_code: str) -> InlineKeyboardMarkup:
    kb_rows: list[list[InlineKeyboardButton]] = []

    for code, title in PROTOCOLS:
        kb_rows.append(
            [
                InlineKeyboardButton(
                    text=title,
                    callback_data=MenuCb(
                        section="proto",
                        action="open",
                        target=f"{device_code}|{code}",
                    ).pack(),
                )
            ]
        )

    kb_rows.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=MenuCb(section="instr", action="open").pack(),
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=kb_rows)


def kb_proto_back(device_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=MenuCb(
                        section="device", action="open", target=device_code
                    ).pack(),
                )
            ]
        ]
    )


def kb_ref_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💱 Обмен баллов",
                    callback_data=MenuCb(section="exch", action="open").pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=MenuCb(section="main", action="open").pack(),
                )
            ],
        ]
    )


def kb_exchange_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=MenuCb(section="ref", action="open").pack(),
                )
            ]
        ]
    )


def kb_settings_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=MenuCb(section="main", action="open").pack(),
                )
            ]
        ]
    )


def kb_rules_back() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=MenuCb(section="info", action="open").pack(),
                )
            ]
        ]
    )
