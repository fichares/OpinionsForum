from urllib import request

from django import forms
from .models import User, Notes, Files
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter login'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Repeat password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(help_text='Login', widget=forms.TextInput(attrs={'class': 'form-input', 'size': '30', 'rows':'25', 'placeholder': 'Enter name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'size': '30', 'rows':'25', 'placeholder': 'Enter password'}))


class Create_New_notes(forms.ModelForm):

    topic = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Enter topic'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input', 'size': '30', 'rows':'25', 'placeholder': 'Enter text'}))

    def __init__(self, *args, **kwargs):
        super(Create_New_notes, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['topic'].widget.attrs['style'] = 'width:650px; height:20px;'
        self.fields['text'].widget.attrs['style'] = 'width:650px; height:80px;'

    class Meta:
        model = Notes
        fields = ('topic', 'text')


class ViewNote(Create_New_notes):
    pass

class ViewFile(forms.ModelForm):
    name =  forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter topic'}))
    files = forms.FileField()
    class Meta:
        model = Files
        fields = ('name', 'files')



class CreateFile(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter name'}))
    files = forms.FileField()
    class Meta:
        model = Files
        fields = ('name', 'files')