from django.db import models
from django.db import models


class User(models.Model):
    """
    Пользователь Telegram.

    Хранит:
    - telegram_id — уникальный ID пользователя в Telegram.
    - username — Telegram username (если есть).
    - created_at — дата первого входа в бот.

    Username может отсутствовать, поэтому используется null=True.
    """

    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username or str(self.telegram_id)


class Plan(models.Model):
    """
    Тариф VPN-сервиса.

    Пример тарифов:
    - Basic (5 устройств)
    - Family (15 устройств)
    - Corporate (до N устройств)

    Поля:
    - name — название тарифа
    - max_devices — количество одновременно доступных устройств
    - price — стоимость тарифа (в любой валюте, например Stars)
    """

    name = models.CharField(max_length=50)
    max_devices = models.IntegerField()
    price = models.IntegerField()

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """
    Активная подписка пользователя.

    Содержит:
    - user — владелец подписки
    - plan — тарифный план
    - status — active/expired/blocked
    - expires_at — дата окончания подписки

    on_delete=PROTECT для планов, чтобы нельзя было удалить тариф,
    к которому привязаны подписки.
    """

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('blocked', 'Blocked'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    expires_at = models.DateTimeField()

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user} → {self.plan} ({self.status})"


class Server(models.Model):
    """
    Xray/VLESS сервер VPN-сети.

    Содержит:
    - name — имя сервера (например: 'Germany #1')
    - region — страна/регион
    - host — домен или IP
    - port — порт входящего соединения
    - is_active — можно ли использовать этот сервер
    """

    name = models.CharField(max_length=100)
    region = models.CharField(max_length=50)
    host = models.CharField(max_length=255)
    port = models.IntegerField(default=443)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Сервер"
        verbose_name_plural = "Серверы"

    def __str__(self):
        return f"{self.region} — {self.host}"


class Device(models.Model):
    """
    Слот устройства.

    Каждый слот — это уникальный UUID (ключ доступа),
    который пользователь использует на одном устройстве.

    Поля:
    - subscription — подписка, к которой привязан слот
    - user — владелец слота
    - device_label — название устройства (Телефон, ПК, iPad…)
    - uuid — уникальный ключ (для Xray)
    - revoked — слот заблокирован
    """

    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_label = models.CharField(max_length=255, null=True, blank=True)
    uuid = models.CharField(max_length=255, unique=True)
    revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Устройство"
        verbose_name_plural = "Устройства"

    def __str__(self):
        return f"{self.user} — {self.device_label or self.uuid}"


class ActiveSession(models.Model):
    """
    Активная VPN-сессия устройства.

    Обновляется агентом на сервере каждые N секунд.

    Поля:
    - server — сервер, к которому подключено устройство
    - device — слот устройства (с UUID)
    - user — владелец
    - ip_address — IP клиента
    - last_seen — время последнего обнаружения (heartbeat)

    Используется для контроля лимита "не более N устройств онлайн".
    """

    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Активная сессия"
        verbose_name_plural = "Активные сессии"

    def __str__(self):
        return f"{self.user} @ {self.server}"
