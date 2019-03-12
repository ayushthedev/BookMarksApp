from django import forms
from django.contrib.auth.models import User
from .models import Profile
from string import Template
from django.utils.safestring import mark_safe
# from

class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None,renderer=None):
        html = Template("""<img src="$link"/>""")
        print('___________________________')
        return mark_safe(html.substitute(link=value))

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput,label='Confirmed Password')

    class Meta:
        model = User
        fields =('username','first_name','email')

    def _clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords dont Match')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    photo = forms.ImageField()
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')

