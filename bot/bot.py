import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.client.default import DefaultBotProperties

# ====== ⚙️ Конфиг ======

BOT_TOKEN = "8138921040:AAFD70P8BxybtG3gv00glIijTBx5dcFidGY"  # TODO: вынести в .env / настройки
MAIN_MENU_PHOTO_ID = "https://picsum.photos/600/400"  # TODO: заменить на реальный file_id

logging.basicConfig(level=logging.INFO)

# ====== 📦 CallbackData для меню ======

class MenuCb(CallbackData, prefix="menu"):
    """
    CallbackData для навигационного меню.

    section: главный раздел/экран (main, pay, info, instr, rules, ref, exch, settings, device, proto)
    action: поддействие (open, tariff и т.п.)
    target: дополнительные данные (код тарифа, устройства, протокола)
    """
    section: str
    action: str | None = None
    target: str | None = None


# ====== 🧱 Константы ======

DEVICES = [
    ("iphone_ipad", "📱 iPhone / iPad"),
    ("android", "🤖 Android"),
    ("mac", "💻 macOS"),
    ("windows", "🖥 Windows"),
    ("linux", "🐧 Linux"),
    ("androidtv", "📺 Android TV"),
    ("appletv", "🍎 Apple TV"),
]

PROTOCOLS = [
    ("vless", "VLESS"),
    ("outline", "Outline"),
]

TARIFFS = [
    ("tariff1", "Тариф 1"),
    ("tariff2", "Тариф 2"),
    ("tariff3", "Тариф 3"),
]


# ====== 🧷 Клавиатуры ======

def kb_main_menu() -> InlineKeyboardMarkup:
    """Главное меню."""
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
    """Меню тарифов в разделе 'Оплата' + Назад → главное меню."""
    buttons_row1 = [
        InlineKeyboardButton(
            text=title,
            callback_data=MenuCb(section="pay", action="tariff", target=code).pack(),
        )
        for code, title in TARIFFS[:2]
    ]
    buttons_row2 = []
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

    # Назад → в главное меню
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
    """Меню раздела 'Информация' + Назад → главное меню."""
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
    """Список устройств в инструкции + Назад → Информация."""
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

    # Назад → в раздел "Информация"
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
    """
    Список протоколов для выбранного устройства + Назад → Инструкция.
    Используется на экране "Инструкция → Устройство".
    """
    kb_rows: list[list[InlineKeyboardButton]] = []

    for code, title in PROTOCOLS:
        kb_rows.append(
            [
                InlineKeyboardButton(
                    text=title,
                    callback_data=MenuCb(
                        section="proto", action="open", target=f"{device_code}|{code}"
                    ).pack(),
                )
            ]
        )

    # Назад → список устройств (Инструкция)
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
    """
    Клавиатура для экрана конкретного протокола.
    Назад → экран устройства (список протоколов).
    """
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
    """Меню 'Реферальная программа' + Назад → главное меню."""
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
    """Меню 'Обмен баллов' + Назад → Реферальная программа."""
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
    """Меню 'Настройки' + Назад → главное меню."""
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
    """Кнопка Назад на экране правил → в раздел 'Информация'."""
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


# ====== 🧠 Тексты (заглушки) ======

def main_menu_caption(user: Message | CallbackQuery) -> str:
    """Текст главного меню с ID пользователя."""
    from_user = user.from_user if isinstance(user, Message) else user.from_user
    return (
        "👋 Добро пожаловать в VPN-сервис!\n\n"
        f"🆔 Ваш ID: <code>{from_user.id}</code>\n\n"
        "🔗 Гайды по настройке: https://example.com/guides  TODO: заменить ссылку"
    )


def pay_text() -> str:
    """Текст раздела 'Оплата'."""
    return (
        "💳 *Оплата и тарифы*\n\n"
        "Тут будет описание тарифов и условий подписки.\n"
        "Выберите тариф, чтобы продолжить."
    )


def info_text() -> str:
    """Текст раздела 'Информация'."""
    return (
        "ℹ️ *Информация о боте*\n\n"
        "Здесь кратко описываем, как работает сервис, чем он отличается, и т.д."
    )


def instruction_intro_text() -> str:
    """Текст вступления к разделу 'Инструкция'."""
    return (
        "📘 *Инструкция по настройке*\n\n"
        "Выберите устройство, для которого хотите получить гайд.\n"
        "_Этот текст от разработчика: тут можно рассказать о нюансах и общих шагах._"
    )


def rules_text() -> str:
    """Текст правил сервиса (заглушка)."""
    return (
        "📜 *Правила сервиса*\n\n"
        "1. Не нарушать законы своей страны.\n"
        "2. Не передавать доступ третьим лицам.\n"
        "3. Не использовать сервис для спама, DDoS и прочей дичи.\n\n"
        "_Здесь будут реальные правила сервиса._"
    )


def device_text(device_code: str) -> str:
    """Текст экрана выбранного устройства."""
    title = next((t for c, t in DEVICES if c == device_code), device_code)
    return (
        f"{title}\n\n"
        "Выберите протокол, который хотите использовать для этого устройства."
    )


def proto_text(device_code: str, proto_code: str) -> str:
    """Текст экрана конкретного протокола для устройства."""
    device_title = next((t for c, t in DEVICES if c == device_code), device_code)
    proto_title = next((t for c, t in PROTOCOLS if c == proto_code), proto_code)
    return (
        f"📘 Инструкция для *{device_title}* через *{proto_title}*\n\n"
        "_Здесь будет подробный шаг-за-шагом гайд по подключению._"
    )


def ref_text(user: Message | CallbackQuery) -> str:
    """Текст раздела 'Реферальная программа'."""
    from_user = user.from_user if isinstance(user, Message) else user.from_user
    return (
        "👥 *Реферальная программа*\n\n"
        "Ваша реферальная ссылка:\n"
        f"`https://t.me/your_bot?start=ref_{from_user.id}`\n\n"
        "Реферальная статистика:\n"
        "- Приглашено: 0\n"
        "- Активных подписок: 0\n"
        "- Баллов: 0\n\n"
        "_Тут будут реальные данные из БД._"
    )


def exchange_text() -> str:
    """Текст раздела 'Обмен баллов'."""
    return (
        "💱 *Обмен баллов на подписку*\n\n"
        "Например:\n"
        "- 100 баллов = 1 неделя подписки\n"
        "- 300 баллов = 1 месяц подписки\n\n"
        "_Тут будут реальные курсы обмена._"
    )


def settings_text() -> str:
    """Текст раздела 'Настройки'."""
    return (
        "⚙️ *Настройки*\n\n"
        "Здесь будут настройки аккаунта: язык, уведомления, автооплата и т.п."
    )


# ====== 📡 Роутеры ======

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    /start — старт/рестарт бота.
    Показывает главное меню с приветствием.
    """
    await message.answer_photo(
        MAIN_MENU_PHOTO_ID,
        caption=main_menu_caption(message),
        reply_markup=kb_main_menu(),
    )


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    """
    /menu — принудительно показать главное меню.
    """
    await message.answer_photo(
        MAIN_MENU_PHOTO_ID,
        caption=main_menu_caption(message),
        reply_markup=kb_main_menu(),
    )


# ====== 🔁 Навигация по меню (callback handlers) ======

@router.callback_query(MenuCb.filter(F.section == "main"))
async def cb_main_menu(call: CallbackQuery, callback_data: MenuCb):
    """
    Любая кнопка, ведущая в главное меню.
    Просто отправляет новое сообщение с главным меню.
    """
    try:
        await call.message.delete()
    except Exception:
        pass

    await call.message.answer_photo(
        MAIN_MENU_PHOTO_ID,
        caption=main_menu_caption(call),
        reply_markup=kb_main_menu(),
    )
    await call.answer()


@router.callback_query(MenuCb.filter(F.section == "pay"))
async def cb_pay(call: CallbackQuery, callback_data: MenuCb):
    """
    Раздел 'Оплата'.
    Если нажали на тариф — пока просто показываем заглушку.
    Иначе — показываем список тарифов.
    """
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


@router.callback_query(MenuCb.filter(F.section == "info"))
async def cb_info(call: CallbackQuery, callback_data: MenuCb):
    """
    Раздел 'Информация'.
    """
    await call.message.edit_caption(
        caption=info_text(),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb_info_menu(),
    )
    await call.answer()


@router.callback_query(MenuCb.filter(F.section == "instr"))
async def cb_instruction(call: CallbackQuery, callback_data: MenuCb):
    """
    Раздел 'Инструкция' — список устройств.
    """
    await call.message.edit_caption(
        caption=instruction_intro_text(),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb_instruction_devices(),
    )
    await call.answer()


@router.callback_query(MenuCb.filter(F.section == "rules"))
async def cb_rules(call: CallbackQuery, callback_data: MenuCb):
    """
    Раздел 'Правила сервиса'.
    Назад → в 'Информацию'.
    """
    await call.message.edit_caption(
        caption=rules_text(),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb_rules_back(),
    )
    await call.answer()


@router.callback_query(MenuCb.filter(F.section == "device"))
async def cb_device(call: CallbackQuery, callback_data: MenuCb):
    """
    Экран 'Инструкция → Устройство'.
    Показывает список протоколов для выбранного устройства.
    """
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
    target в формате "device:proto".
    """
    if not callback_data.target or ":" not in callback_data.target:
        await call.answer("Некорректные данные", show_alert=True)
        return

    device_code, proto_code = callback_data.target.split("|", 1)
    await call.message.edit_caption(
        caption=proto_text(device_code, proto_code),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb_proto_back(device_code),
    )
    await call.answer()


@router.callback_query(MenuCb.filter(F.section == "ref"))
async def cb_ref(call: CallbackQuery, callback_data: MenuCb):
    """
    Раздел 'Реферальная программа'.
    Назад → в главное меню.
    """
    await call.message.edit_caption(
        caption=ref_text(call),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb_ref_menu(),
    )
    await call.answer()


@router.callback_query(MenuCb.filter(F.section == "exch"))
async def cb_exchange(call: CallbackQuery, callback_data: MenuCb):
    """
    Раздел 'Обмен баллов'.
    Назад → в 'Реферальную программу'.
    """
    await call.message.edit_caption(
        caption=exchange_text(),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb_exchange_menu(),
    )
    await call.answer()


@router.callback_query(MenuCb.filter(F.section == "settings"))
async def cb_settings(call: CallbackQuery, callback_data: MenuCb):
    """
    Раздел 'Настройки'.
    Назад → в главное меню.
    """
    await call.message.edit_caption(
        caption=settings_text(),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb_settings_menu(),
    )
    await call.answer()


# ====== 🚀 Запуск ======

async def main():
    """Инициализация и запуск бота в режиме long polling."""
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)

    # === Устанавливаем команды в Telegram ===
    await bot.set_my_commands(
        commands=[
            {"command": "menu", "description": "Главное меню"},
        ]
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
