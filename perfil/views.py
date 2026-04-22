from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views import View
from django.contrib.auth import authenticate, login

from . import forms
from . import models

class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        perfil_instance = getattr(self.request.user, 'perfil', None)

        if self.request.user.is_authenticated:           
            self.contexto = {
                'user_form': forms.UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user,
                    ),
                'perfil_form': forms.PerfilForm(
                    data=self.request.POST or None,
                    instance=perfil_instance
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

    def salvar_usuario(self, user_form):
        usuario = user_form.save(commit=False)

        password = user_form.cleaned_data.get('password')
        if password:
            usuario.set_password(password)
        usuario.save()
        return usuario

    def salvar_perfil(self, perfil_form, usuario):
        perfil = perfil_form.save(commit=False)
        perfil.usuario = usuario
        perfil.save()
        return perfil
    
    def autenticar_usuario(self, request, username, password):
        if not password:
            return
        
        carrinho = self.request.session.get('carrinho', {})

        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            login(request, usuario)
            request.session['carrinho'] = carrinho
            request.session.save()

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, self.contexto)
    
    def post(self, *args, **kwargs):
        user_form = self.contexto['user_form']
        perfil_form = self.contexto['perfil_form']

        if user_form.is_valid() and perfil_form.is_valid():

            if self.request.user.is_authenticated:
                usuario = user_form.save(commit=False)
            else:
                usuario = user_form.save(commit=False)

            password = user_form.cleaned_data.get('password')
            if password:
                usuario.set_password(password)

            usuario = self.salvar_usuario(user_form)

            self.salvar_perfil(perfil_form, usuario)

            if not self.request.user.is_authenticated:
                self.autenticar_usuario(self.request,
                                    user_form.cleaned_data.get('username'),
                                    user_form.cleaned_data.get('password')
                                    )
            
            return redirect('perfil:atualizar')
        
        return render(self.request, self.template_name, self.contexto)



class Criar(BasePerfil):
        pass
    
    
class Atualizar(View):
    pass

class Login(View):
    pass

class Logout(View):
    pass


