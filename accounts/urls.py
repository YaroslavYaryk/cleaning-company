from django.urls import path
from .views import LoginUser, RegisterUser, LogoutUser
from .views import get_profile_edit, get_profile, change_password

urlpatterns = [
    path("login/", LoginUser.as_view(), name="login"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("logout/", LogoutUser.as_view(), name="logout"),
    path("profile/", get_profile, name="profile"),
    path("profile_edit", get_profile_edit, name="edit_profile"),
    path("change_password/", change_password, name="change_password"),
]
