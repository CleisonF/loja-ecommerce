from django import forms
from django.contrib.auth.models import User
from . import models





class PerfilForm (forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = ['__all__']
        exclude = ('usuario',)

class UserForm (forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name','password']

