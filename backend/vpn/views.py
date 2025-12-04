from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Device
from .serializers import DeviceSerializer


class DevicesView(APIView):
    """
    API endpoint для получения списка всех устройств.

    Использование:
    - GET /api/devices/

    Возвращает сериализованный список всех Device в базе.

    Этот endpoint используется:
    - на этапе разработки (чтобы проверить работу моделей/сериалайзеров),
    - для тестирования выдачи устройств,
    - может быть расширен фильтрацией по пользователю, подписке или статусу.

    В продакшене сюда обычно добавляется:
    - аутентификация бота через токен,
    - фильтрация по текущему пользователю,
    - проверка прав доступа.
    """

    def get(self, request):
        """
        Возвращает JSON со всеми устройствами.

        Пример ответа:
        [
            {
                "id": 1,
                "subscription": 3,
                "user": 7,
                "uuid": "ab34c1d2...",
                "device_label": "Телефон",
                "revoked": false,
                "created_at": "2025-11-27T14:52:10Z"
            }
        ]
        """
        devices = Device.objects.all()
        return Response(DeviceSerializer(devices, many=True).data)
