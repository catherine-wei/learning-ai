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
    '''
    设置 JavaScript 的 Content-Type
    FIXME 这个中间件对静态文件不起作用，如果要让这个中间件工作起来的话，必须在settings.py禁用 django.contrib.staticfiles
    '''
    def __init__(self, get_response):
        self.get_response = get_response
 
    def __call__(self, request):
        response = self.get_response(request)
        # 获取请求的路径
        request_path = request.path

        # 根据请求路径决定是否修改 Content-Type
        if request_path.startswith('/threevrm/') and request_path.endswith('.js'):
            response['Content-Type'] = 'text/javascript'
        return response
    