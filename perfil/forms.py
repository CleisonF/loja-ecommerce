from django import forms
from django.contrib.auth.models import User
from . import models





class PerfilForm (forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)

class UserForm (forms.ModelForm):

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Deixe em branco para manter a senha atual'}),
        label='Senha',
    )
    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name','password']

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_messages = {}

        if self.usuario:
            usuario = User.objects.filter(username=cleaned.get('username')).exclude(pk=self.usuario.pk)
        else:
            usuario = User.objects.filter(username=cleaned.get('username'))

        if validation_error_messages:
            raise forms.ValidationError(validation_error_messages)