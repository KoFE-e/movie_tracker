from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': 'Введите логин'}))
    password1 = forms.CharField(label='Пароль', widget=forms.TextInput(attrs={'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.TextInput(attrs={'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        cd = self.cleaned_data
        if len(cd['username']) < 3:
            raise forms.ValidationError('Длина логина должна быть не менее 3 символов')
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('Такой пользователь уже существует')
        return cd['username']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        if len(cd['password2']) < 4:
            raise forms.ValidationError('Длина пароля должна быть не менее 4 символов')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', min_length=3, widget=forms.TextInput(attrs={'placeholder': 'Введите логин'}))
    password = forms.CharField(label='Пароль', min_length=4, widget=forms.TextInput(attrs={'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Неправильный логин или пароль")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
