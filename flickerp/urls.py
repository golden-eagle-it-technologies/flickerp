from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("lists/", include("task.urls")),
    # url(r'^admin/', include(admin.site.urls)),
    # url(r'^admin/', include(admin_reports.site.urls)),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]
