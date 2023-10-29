from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from Users import views

urlpatterns = [
    path('', include('Taster.urls')),
    path('user/', include('Users.urls')),
    path('admin/ajax-request-reset', views.admin_ajax_request, name='admin_ajax'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'Taster.views.view_404'
