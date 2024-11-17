import random
import string
import secrets
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView

from config.settings import EMAIL_HOST_USER
from catalog.views import UserLoginRequiredMixin
from users.forms import UserRegisterForm, ProfileForm, ResetPasswordForm
from users.models import User

from mailing.models import Mailing, Client
from blog.models import Blog

from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def home(request):

    mailings = Mailing.objects.filter(owner=request.user)
    # Получение общего количества рассылок
    total_mailings = mailings.count()

    # Получение количества рассылок со статусом RUNNING
    running_mailings = mailings.filter(status='R').count()

    # Получение количества клиентов, принадлежащих текущему пользователю
    user_clients = Client.objects.filter(owner=request.user).count()

    # Получение трех случайных постов из модели Post
    random_posts = Blog.objects.order_by('?')[:3]

    context = {
        'total_mailings': total_mailings,
        'running_mailings': running_mailings,
        'user_clients': user_clients,
        'random_posts': random_posts,
    }

    return render(request, 'users/main.html', context)  # Отображение main.html для авторизованных пользователей

def login_view(request):
    return render(request, 'users/login.html')  # Отображение login.html для неавторизованных пользователей


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Перейдите по ссылке для подтверждения {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserResetPasswordView(UserLoginRequiredMixin, PasswordResetView):
    form_class = ResetPasswordForm
    template_name = "users/reset_password.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            if user:
                password = User.objects.make_random_password(length=10)
                user.set_password(password)
                user.save()
                send_mail(
                    subject="Сброс пароля",
                    message=f" Ваш новый пароль {password}",
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
            return redirect(reverse("users:login"))
        except:
            return redirect(reverse("users:wrong_email"))


class NotMailPageView(UserLoginRequiredMixin, TemplateView):
    template_name = "users/wrong_email.html"


def generate_random_password(length=8):
    """Генерирует случайный пароль."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


def user_list(request):
    user = request.user
    if user.is_authenticated and user.groups.filter(name='manager').exists():
        users = User.objects.all()
        return render(request, 'users/user_list.html', {'users': users})
    raise PermissionDenied


def toggle_activation(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = not user.is_active
    user.save()

    action = 'активирован' if user.is_active else 'деактивирован'
    messages.success(request, f'Пользователь {user.email} был {action}.')

    return redirect('users:user_list')  # Перенаправляем обратно в список пользователей


def toggle_activation(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = not user.is_active
    user.save()

    action = 'активирован' if user.is_active else 'деактивирован'
    messages.success(request, f'Пользователь {user.email} был {action}.')

    return redirect('users:user_list')  # Перенаправляем обратно в список пользователей