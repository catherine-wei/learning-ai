# 在你的 Django 应用中的 middleware.py 文件中
 
import string
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
 
class PrintRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("Request Method:", request.method)
        if request.method == 'POST':
            csrf_token = request.META.get('CSRF_COOKIE')
            print(f"Request POST:csrf={csrf_token}, data={request.POST}")

        else:
            print("Request body:", request.body)

class DisableCSRF(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

class SetJavaScriptContentTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
 
    def __call__(self, request):
        print(f"request={request}")
        response = self.get_response(request)
        if response['Content-Type'] == 'text/plain':  # 仅当是HTML响应时修改（可选）
            response['Content-Type'] = 'text/javascript'
        return response