"""
URL configuration for cwchat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf.urls.static import static

from chat.views.views_3d import CharacterView
from chat.views.views import talk_view, show_urls_view

schema_view = get_schema_view(
    openapi.Info(
        title="CatherineBot API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="catherine@oddmeta.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('show_urls/', show_urls_view, name='show_urls'),

    # path('admin/', admin.site.urls),
    path('admin/', include("chat.urls_admin")),
    path("chat/", include("chat.urls")),
    path("threevrm/", include("chat.urls_three")),

    path('', CharacterView.default, name='home'),

    path('talk.html', talk_view, name='talk_view'),
    path('test3d.html', CharacterView.test3d, name='test3d'),
    path('test3vrm.html', CharacterView.test3vrm, name='test3vrm'),
    path('test3vrm2.html', CharacterView.test3vrm2, name='test3vrm2'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
