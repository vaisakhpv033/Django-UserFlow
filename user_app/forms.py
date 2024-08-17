from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'id': 'username',
        'type': 'text',
        'required': '',
    }),
    required=True
    )
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
        'id': 'password',
        'type': 'password',
        'required': ''
    }), 
    required=True
    )



class SignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'id': 'username',
        'required': '',
    }),
    required=True,
    max_length=50
    )

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg',
        'id': 'email',
        'type': 'email',
        'required': '',
    }),
    required=True
    )

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
        'id': 'password',
        'type': 'password',
        'required': '',
    }),
    required=True
    )

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
        'id': 'password',
        'type': 'password',
        'required': '',
    }),
    required=True
    )

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'id': 'first_name',
        'type': 'text',
        'required': '',
    }),
    max_length=50,
    min_length=3,
    required=True
    )

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'id': 'first_name',
        'type': 'text',
        'required': '',
    }),
    max_length=50,
    required=True
    )


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']


    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email