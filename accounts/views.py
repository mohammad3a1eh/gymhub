from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.utils.timezone import now




class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        return self.request.user


class PasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('profile')


def custom_register(request):
    if request.method == "GET":
        return redirect('home')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "ثبت نام شما با موفقیت انجام شد!")
            login(request, user)
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
            return redirect('home')


def custom_login(request):
    MAX_ATTEMPTS = 5
    LOCKOUT_TIME = 300 

    client_ip = get_client_ip(request)
    cache_key = f"login_attempts_{client_ip}"

    if request.method == "GET":
        return redirect('home')

    if request.method == "POST":
        attempts_data = cache.get(cache_key, {"attempts": 0, "last_attempt": None})
        attempts = attempts_data.get("attempts", 0)
        last_attempt = attempts_data.get("last_attempt")

        if attempts >= MAX_ATTEMPTS:
            time_since_last_attempt = (now() - last_attempt).total_seconds()
            if time_since_last_attempt < LOCKOUT_TIME:
                messages.error(request, f"لطفاً {int(LOCKOUT_TIME - time_since_last_attempt)} ثانیه دیگر تلاش کنید.")
                return redirect('home')
            else:
                cache.set(cache_key, {"attempts": 0, "last_attempt": None})

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, "لطفاً تمام فیلدها را پر کنید.")
            return redirect('home')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            cache.delete(cache_key)
            login(request, user)
            messages.success(request, "شما با موفقیت وارد شدید!")
            return redirect('home')
        else:
            attempts += 1
            cache.set(cache_key, {"attempts": attempts, "last_attempt": now()}, LOCKOUT_TIME)
            messages.error(request, f"اطلاعات ورود صحیح نیست. ({MAX_ATTEMPTS - attempts} تلاش باقی‌مانده)")
            return redirect('home')



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



# coustum logout

def custom_logout(request):
    logout(request)
    messages.success(request, "شما با موفقیت خارج شدید!")
    return redirect('home')