# from django.contrib.auth.models import User
from .models import MyUser


def create_user(username: str, password: str, email: str) -> MyUser:
    user = MyUser(
        username=username,
        email=email,
        # default False field
        is_staff=False,
        is_superuser=False,
    )
    user.set_password(password)
    user.save()
    return user
