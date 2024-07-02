from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from Users import views

urlpatterns = [
    path('', include('Taster.urls')),
    path('user/', include('Users.urls')),
    path('user/', include('django.contrib.auth.urls')),
    path('admin/ajax-request-reset', views.admin_ajax_request, name='admin_ajax'),
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)