from django import forms
from django.contrib.auth.forms import UserCreationForm

from account.models import User


class UserForm(forms.ModelForm):


    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'phone', 'email']


    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        #라벨설정
        self.fields['username'].label = ''
        self.fields['password'].label = ''
        self.fields['name'].label = ''
        self.fields['phone'].label = ''
        self.fields['email'].label = ''

        #인풋설정
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['email'].widget = forms.EmailInput()

        #위젯설정
        self.fields['username'].widget.attrs = {
            'placeholder' : 'ID',
        }

        self.fields['password'].widget.attrs = {
            'placeholder' : 'Password',
        }

        self.fields['name'].widget.attrs = {
            'placeholder' : 'Name',
        }

        self.fields['phone'].widget.attrs = {
            'placeholder' : 'Phone',
        }

        self.fields['email'].widget.attrs = {
            'placeholder': 'E-mail',
        }



class LoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'ID'
    }))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': 'Password'
    }))


class passwordChangeForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

