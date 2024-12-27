from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none input-focus text-gray-700',
            'placeholder': 'Create a password',
            'required': 'required'
        }),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none input-focus text-gray-700',
            'placeholder': 'Confirm your password',
            'required': 'required'
        }),
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(attrs={
            'class': 'mt-4'
        }),
        label="Please verify you are human"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none input-focus text-gray-700',
                'placeholder': 'Enter your first name',
                'required': 'required'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none input-focus text-gray-700',
                'placeholder': 'Enter your last name',
                'required': 'required'
            }),
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none input-focus text-gray-700',
                'placeholder': 'Enter your username',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none input-focus text-gray-700',
                'placeholder': 'Enter your email',
                'required': 'required'
            }),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password and confirm Password don't match!")
        validate_password(password1)
        return password2



from django import forms
from django.contrib.auth import authenticate
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:ring focus:ring-green-300',
            'placeholder': 'Enter your username',
            'required': 'required'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:ring focus:ring-green-300',
            'placeholder': 'Enter your password',
            'required': 'required'
        })
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid username or password.")
            self.user = user  # Save user instance for use in the view

        return cleaned_data
