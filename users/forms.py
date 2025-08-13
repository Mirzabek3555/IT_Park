from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email manzilingiz'}))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon raqamingiz'}))
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    school = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Maktab nomi'}))
    grade = forms.IntegerField(min_value=1, max_value=11, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Sinf'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ismingiz'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiyangiz'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolni tasdiqlang'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'birth_date', 'school', 'grade', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu email allaqachon ro\'yxatdan o\'tgan.')
        return email

class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email manzilingiz'}))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon raqamingiz'}))
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    school = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Maktab nomi'}))
    grade = forms.IntegerField(min_value=1, max_value=11, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Sinf'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ismingiz'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiyangiz'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'birth_date', 'school', 'grade')

class ProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'O\'zingiz haqida qisqacha ma\'lumot...'}))
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'style': 'display: none;'}))

    class Meta:
        model = Profile
        fields = ('avatar', 'bio')
