from django import forms
from Homepage.models import Register

class SignUpForm(forms.ModelForm):
    class Meta():
        model = Register
        exclude = []
        widgets = {
            'Username': forms.TextInput(attrs={'class': 'form-control','id':'inputPassword','placeholder': 'Username'}),
            'Email': forms.TextInput(attrs={'class': 'form-control','id':'inputPassword','placeholder': 'Email'}),
            'Password': forms.TextInput(attrs={'class': 'form-control','id':'inputPassword','placeholder': 'Password'}),
            'VerifyPassword': forms.TextInput(attrs={'class': 'form-control','id':'inputPassword','placeholder': 'VerifyPassword'}),
            'Address': forms.TextInput(attrs={'class': 'form-control','id':'inputPassword','placeholder': 'Address'}),
            'Phone': forms.TextInput(attrs={'class': 'form-control','id':'inputPassword','placeholder': 'Phone'}),
        }

class LoginForm(forms.Form):
    Username = forms.CharField(label='Email',max_length=264,widget=forms.TextInput(attrs={'class': 'form-control','id':'inputPassword','placeholder': 'Username'}))
    Password = forms.CharField(label='LoginId',widget=forms.TextInput(attrs={'class': 'form-control','id':'inputPassword','placeholder': 'Password'}))
