from django.contrib.auth.views import LoginView

from .forms import UserLoginForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True
