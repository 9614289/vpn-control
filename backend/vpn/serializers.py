from rest_framework import serializers
from .models import User, Subscription, Device, Server

class DeviceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Device.

    Используется для:
    - вывода списка устройств пользователя,
    - отображения данных устройств в админ-панели/боте,
    - передачи данных во внешние API (например, node-agent),
    - сериализации данных при выдаче клиентских конфигов.

    Поля включают:
    - id — ID слота устройства
    - subscription — подписка, к которой относится устройство
    - user — владелец устройства
    - uuid — ключ доступа (используется Xray)
    - device_label — название устройства
    - revoked — отключено ли устройство
    - created_at — дата создания
    """
    class Meta:
        model = Device
        fields = [
            "id",
            "subscription",
            "user",
            "device_label",
            "uuid",
            "revoked",
            "created_at",
        ]
