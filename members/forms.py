from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignupForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')
    
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = 'Fantasiename (öffentlich)'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Merk ihn dir fürs Login! _-.+@ erlaubt, keine Lücken'
        self.fields['username'].help_text = ''
        self.fields['password1'].label = 'Passwort'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['type'] = 'password'
        self.fields['password1'].widget.attrs['placeholder'] = 'Mind. 8 Zeichen'
        self.fields['password1'].help_text = ''
        self.fields['password2'].label = 'Passwort wiederholen'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['type'] = 'password'
        self.fields['password2'].help_text = ''
        self.fields['email'].widget.attrs['placeholder'] = 'Für die Passwortwiederherstellung'
