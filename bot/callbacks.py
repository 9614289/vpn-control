from aiogram.filters.callback_data import CallbackData


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
