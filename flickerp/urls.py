from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]
