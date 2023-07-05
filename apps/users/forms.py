from django.contrib.auth import forms, get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CreateUserForm(forms.UserCreationForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User
        exclude = ["username"]
        errors = {"email": {"unique": {_("This email is already taken")}}}


class UpdateUserForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User
        exclude = ["username"]
