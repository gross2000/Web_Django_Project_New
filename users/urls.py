from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from users import views
from users.apps import UsersConfig
from users.views import (
    RegisterView,
    ProfileView,
    email_verification,
    UserResetPasswordView,
    NotMailPageView,
    user_list,
    toggle_activation
)


app_name = UsersConfig.name


urlpatterns = [
    path('', cache_page(60)(views.home), name="home"),
    path("", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("reset-password/", UserResetPasswordView.as_view(), name="reset_password"),
    path("no-email/", NotMailPageView.as_view(), name="no_email"),

    path("profile/", ProfileView.as_view(), name="profile"),
    path("users/", user_list, name="user_list"),
    path("users/toggle/<int:user_id>/", toggle_activation, name='toggle_activation'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# OLD VERSION
# from django.contrib.auth.views import LoginView, LogoutView
# from django.urls import path
#
# from users.apps import UsersConfig
# from users.views import UserCreateView, ProfileView, email_verification, reset_password
#
# app_name = UsersConfig.name
#
# urlpatterns = [
#     path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
#     path("logout/", LogoutView.as_view(), name="logout"),
#     path("register/", UserCreateView.as_view(), name="register"),
#     path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
#     path("profile/", ProfileView.as_view(), name="profile"),
#     path("reset_password/", reset_password, name="reset_password"),
# ]