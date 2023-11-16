from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import (
handler400, handler403, handler404, handler500
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('restaurantapp.urls')),
    path('user/', include('userapp.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
handler400 = 'userapp.views.custom_page_not_found_view'