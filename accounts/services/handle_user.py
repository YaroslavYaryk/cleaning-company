from accounts.models import User


def get_user_by_email(email):
    try:
        return User.objects.get(email=email)
    except Exception:
        return None
