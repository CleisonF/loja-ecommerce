from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.views import View

from . import forms
from . import models

class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        if self.request.user.is_authenticated:           
            self.contexto = {
                'user_form': forms.UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user,
                    ),
                'perfil_form': forms.PerfilForm(
                    data=self.request.POST or None
                    ),
            }
        else:
            self.contexto = {
                'user_form': forms.UserForm(
                    data=self.request.POST or None
                    ),
                'perfil_form': forms.PerfilForm(
                    data=self.request.POST or None
                    ),
            }    

        self.renderizar = render(
            self.request, self.template_name, self.contexto)


    def get (self, *args, **kwargs):
        return self.renderizar



class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        return self.renderizar
    
    
class Atualizar(View):
    pass

class Login(View):
    pass

class Logout(View):
    pass


