from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls.base import reverse, reverse_lazy
from django.views.generic.edit import CreateView

from .forms import ChangeForm, LoginUserForm, RegisterUserForm
from django.utils.translation import gettext_lazy as _


# Create your views here.
class RegisterUser(SuccessMessageMixin, CreateView):
    """Show register form"""

    form_class = RegisterUserForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")
    error_message = "Registration error"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["title"] = "Registration"
        return context


class LoginUser(SuccessMessageMixin, LoginView):

    """Autorization class"""

    form_class = LoginUserForm
    template_name = "accounts/login.html"
    error_message = "Something went wrong"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["title"] = "Sign in"
        return context


class LogoutUser(LogoutView, SuccessMessageMixin):

    next_page = "home"
    success_message = "Logout successfully"
