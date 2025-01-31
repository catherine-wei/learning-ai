from django.urls import path

from django.http import HttpResponse, HttpResponseNotFound
import os
import mimetypes

def custom_serve_js_main(request):
    filepath = "main.js"
    print(f"custom_serve_js_main, filepath={filepath}")
    return serve_static_js(request=request, filepath=filepath)

def custom_serve_js_mixamoVRMRigMap(request):
    filepath = "mixamoVRMRigMap.js"
    print(f"custom_serve_js_mixamoVRMRigMap, filepath={filepath}")
    return serve_static_js(request=request, filepath=filepath)

def custom_serve_js_loadMixamoAnimation(request):
    filepath = "loadMixamoAnimation.js"
    print(f"custom_serve_js_loadMixamoAnimation, filepath={filepath}")
    return serve_static_js(request=request, filepath=filepath)

def serve_static_js(request, filepath):
    print(f"serve_static_js, filepath={filepath}")

    # 假设你的静态文件存储在项目的某个已知目录下
    # 这里以项目的根目录为例，但你应该使用 Django 的 STATIC_ROOT 或其他适当的位置
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    full_path = os.path.join(base_dir, 'threevrm', filepath)
    
    # 检查文件是否存在
    if not os.path.exists(full_path):
        return HttpResponseNotFound("File not found")
    
    # 读取文件内容
    with open(full_path, 'rb') as f:
        content = f.read()
    
    # 设置正确的 Content-Type
    content_type, encoding = mimetypes.guess_type(full_path)

    print(f"content_type={content_type}")

    if content_type is None:
        # 如果没有猜到，默认为 application/octet-stream
        content_type = 'application/octet-stream'
    elif content_type.startswith('text/') and filepath.endswith('.js'):
        # 对于 JS 文件，确保 Content-Type 是 application/javascript
        content_type = 'application/javascript'
    
    response = HttpResponse(content, content_type=content_type)
    return response

urlpatterns = [
    path('loadMixamoAnimation.js', custom_serve_js_loadMixamoAnimation),
    path('mixamoVRMRigMap.js', custom_serve_js_mixamoVRMRigMap),
    path('main.js', custom_serve_js_main),
    # path('<str:filepath>', serve_static_js, name='serve_static_js'),
]