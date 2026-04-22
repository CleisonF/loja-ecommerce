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
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite a senha de pelo menos 8 caracteres'}
            ),
        label='Senha',
    )

    password_confirmation = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme a senha'}
            ),
        label='Confirmação de senha',    
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name','password',
                  'password_confirmation']

    def clean(self):
        
        cleaned = self.cleaned_data
        validation_error_messages = {}

        usuario_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password_confirmation_data = cleaned.get('password_confirmation')

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Já existe um usuário com esse nome.'
        error_msg_email_exists = 'Já existe um usuário com esse email.'
        error_msg_passwords_do_not_match = 'As senhas não coincidem.'
        error_msg_password_short = 'A senha deve conter pelo menos 8 caracteres.'


        #Usuario logado: atualização de dados
        if self.usuario:
            if usuario_db and usuario_db != self.usuario:
                validation_error_messages['username'] = error_msg_user_exists

            if email_db and email_db != self.usuario:
                validation_error_messages['email'] = error_msg_email_exists

            if password_data:
                if len(password_data) < 8:
                    validation_error_messages['password'] = error_msg_password_short

                if not password_confirmation_data:
                    validation_error_messages['password_confirmation'] = 'Este campo é obrigatório.'
                elif password_data != password_confirmation_data:
                    validation_error_messages['password_confirmation'] = error_msg_passwords_do_not_match

        else:
            if usuario_db:
                validation_error_messages['username'] = error_msg_user_exists

            if email_db:
                validation_error_messages['email'] = error_msg_email_exists

            if not password_data:
                validation_error_messages['password'] = 'Este campo é obrigatório.'

            elif len(password_data) < 8:
                validation_error_messages['password'] = error_msg_password_short

            if password_data:
                if not password_confirmation_data:
                    validation_error_messages['password_confirmation'] = 'Este campo é obrigatório.'
                elif password_data != password_confirmation_data:
                    validation_error_messages['password_confirmation'] = error_msg_passwords_do_not_match

        if validation_error_messages:
            raise forms.ValidationError(validation_error_messages)
        
        return cleaned
    
    def save(self, commit=True):
        usuario = super().save(commit=False)

        password_data = self.cleaned_data.get('password')

        if password_data:
            usuario.set_password(password_data)

        if commit:
            usuario.save()

        return usuario
    