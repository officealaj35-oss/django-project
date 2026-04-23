from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from shop.views import create_admin

urlpatterns = [
    path('admin/', admin.site.urls),

    path('shop/', include('shop.urls')),

    # homepage
    path('', include('blog.urls')),

    # optional
    path('create_admin/', create_admin),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)