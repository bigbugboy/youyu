from django.core.cache import cache
from django.http.response import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

from .utils import get_client_ip


class IPRateLimitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = get_client_ip(request)
        key = f'ip_rate_limit_{ip}'
        count = cache.get(key, 0)
        if count >= 1000:
            return HttpResponseForbidden('ip blocked')
            
        cache.set(key, count + 1, 60)       # 60s
