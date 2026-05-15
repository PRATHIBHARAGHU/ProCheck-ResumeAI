from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-white placeholder-gray-400 transition-all',
        'placeholder': '••••••••'
    }))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-white placeholder-gray-400 transition-all',
        'placeholder': '••••••••'
    }))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-white placeholder-gray-400 transition-all',
                'placeholder': 'johndoe'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-white placeholder-gray-400 transition-all',
                'placeholder': 'john@example.com'
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match.")
        return cleaned_data