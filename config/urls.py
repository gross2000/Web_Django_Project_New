from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('users.urls', namespace='users')),
    path('', include("catalog.urls", namespace="catalog")),
    path("mailing/", include('mailing.urls', namespace="mailing")),
    path('blog/', include('blog.urls', namespace='blog')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""эта часть "+..." из урока sky
Важно! здесь аргумент settings всегда тот, который был указан при запуске проекта!"""