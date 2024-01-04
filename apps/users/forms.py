from django.contrib.auth import forms, get_user_model

User = get_user_model()


class CreateUserForm(forms.UserCreationForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User
        exclude = ["username"]
        errors = {"email": {"unique": {"Этот адрес эл. почты уже заргистрирован"}}}


class UpdateUserForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User
        exclude = ["username"]
