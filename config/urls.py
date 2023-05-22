from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="web接口文档平台",  # 必传
        default_version='v1',  # 必传
        description="接口文档",
        terms_of_service="http://127.0.0.1",
        contact=openapi.Contact(email="wzybmw888@163.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),   # 权限类
)

urlpatterns = [
    path('', RedirectView.as_view(url='redoc/')), # 重定向到/home/
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path("api/v1/", include("config.api_router")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
