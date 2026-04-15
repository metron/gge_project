import logging
from django.http import HttpResponseForbidden
from django.urls import reverse


# Получаем наш логгер, настроенный в settings.py
logger = logging.getLogger('admin_security')

class AdminIPRestrictMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Список разрешенных IP (в реальности лучше вынести в settings.py)
        self.ALLOWED_IPS = ['127.0.0.1', '192.168.0.13']

    def __call__(self, request):
        # Обычный проход запроса дальше
        return self.get_response(request)

    def get_client_ip(self, request):
        # Проверяем заголовок X-Forwarded-For
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Это список IP через запятую, первый — это клиент
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            # Если прокси нет, берем обычный адрес
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Проверяем, ведет ли текущий путь в админку
        # reverse('admin:index') обычно возвращает '/admin/'
        if request.path.startswith(reverse('admin:index')):
            ip = self.get_client_ip(request)
            if ip not in self.ALLOWED_IPS:
                # Если IP нет в списке, возвращаем 403 ошибку
                # Сама view_func (админка) даже не запустится
                logger.warning(f"Отказ в доступе! IP: {ip}, Путь: {request.path}")
                return HttpResponseForbidden(f"Доступ к админке с вашего IP {ip} запрещен.")

        # Если это не админка или IP верный, возвращаем None (запрос идет дальше)
        return None
