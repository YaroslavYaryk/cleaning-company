from django.http.response import HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls.base import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from .services import handle_user
from .forms import ChangeForm, LoginUserForm, RegisterUserForm
from django.utils.translation import gettext_lazy as _


# Create your views here.
class RegisterUser(SuccessMessageMixin, CreateView):
    """Show register form"""

    form_class = RegisterUserForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")
    error_message = "Registration error"

    def dispatch(self, *args, **kwargs):
        dispatch_method = super(RegisterUser, self).dispatch

        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))

        return dispatch_method(*args, **kwargs)

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

    def dispatch(self, *args, **kwargs):
        dispatch_method = super(LoginUser, self).dispatch

        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))

        return dispatch_method(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        try:

            username = kwargs.get("data").get("username")
            user_active = handle_user.get_user_by_email(username).is_active
            if not user_active:
                messages.error(self.request, "Unfortunatelly this user is unactive")
        except Exception:
            pass
        return kwargs

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["title"] = "Sign in"
        return context


class LogoutUser(LogoutView, SuccessMessageMixin):

    next_page = "home"
    success_message = "Logout successfully"
