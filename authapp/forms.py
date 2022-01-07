import hashlib
import random
from datetime import datetime

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, ValidationError, UserChangeForm
from django.forms import HiddenInput, ModelForm

from authapp.models import ShopUser, ShopUserProfile


class ShopUserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form_control'

    class Meta:
        model = ShopUser
        fields = ('username', 'password',)


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'email', 'age', 'avatar', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form_control'

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf-8')).hexdigest()
        user.activation_key_expired = datetime.now()
        user.save()
        return user

    def clean_age(self):
        data_age = self.cleaned_data['age']
        if data_age < 18:
            raise ValidationError('You are too young. Age should be >= 18')
        return data_age


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'email', 'age', 'password', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form_control'
            if field_name == 'password':
                field.widget = HiddenInput()

    def clean_age(self):
        data_age = self.cleaned_data['age']
        if data_age < 18:
            raise ValidationError('You are too young. Age should be >= 18')
        return data_age


class ShopUserProfileForm(ModelForm):
    class Meta:
        model = ShopUserProfile
        fields = ('tag_lines', 'about_me', 'gender', 'github_profile')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form_control'

