from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls',namespace='catalog')),
    path("users/", include("users.urls", namespace="users"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



"""эта часть "+..." из урока sky
Важно! здесь аргумент settings всегда тот, который был указан при запуске проекта!"""