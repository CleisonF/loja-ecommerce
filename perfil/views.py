from django.contrib import messages

from django.utils.http import url_has_allowed_host_and_scheme

from django.shortcuts import redirect, render

from django.views import View
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from copy import deepcopy
from . import forms


class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        perfil_instance = getattr(self.request.user, 'perfil', None)

        self.user_form = forms.UserForm(
            data=self.request.POST or None,
            usuario=self.request.user if self.request.user.is_authenticated else None,
            instance=self.request.user if self.request.user.is_authenticated else None,
            )

        self.perfil_form = forms.PerfilForm(
            data=self.request.POST or None,
            instance=perfil_instance
        )    
             
        self.contexto = {
            'user_form': self.user_form,
            'perfil_form': self.perfil_form,
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
    
    def autenticar_usuario(self, usuario):
         
        carrinho = self.request.session.get('carrinho', {})

        login(self.request, usuario)

        self.request.session['carrinho'] = carrinho
        self.request.session.save()
                 

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, self.contexto)
    
    

class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        
        if self.request.user.is_authenticated:
            return redirect('perfil:atualizar')
        
        if self.user_form.is_valid() and self.perfil_form.is_valid():

            usuario = self.salvar_usuario(self.user_form)
            self.salvar_perfil(self.perfil_form, usuario)

            self.autenticar_usuario(usuario)
            messages.success(self.request, 'Cadastro realizado com sucesso!')

            return redirect('produto:lista')
        
        return render(self.request, self.template_name, self.contexto)
    
    
class Atualizar(BasePerfil):
    def post(self, *args, **kwargs):
        
        if not self.request.user.is_authenticated:
            return redirect('perfil:login')
        
        if self.user_form.is_valid() and self.perfil_form.is_valid():
            
            usuario = self.salvar_usuario(self.user_form)

            if self.user_form.cleaned_data.get('password'):
                update_session_auth_hash(self.request, usuario)
            
            self.salvar_perfil(self.perfil_form, usuario)

            messages.success(self.request, 'Perfil atualizado com sucesso!')

            return redirect('perfil:atualizar')
        
        return render(self.request, self.template_name, self.contexto)

class Login(View):
    template_name = 'perfil/login.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)   

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('produto:lista')
        
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        
        
        if not username or not password:
            messages.error(self.request, 'Preencha todos os campos para efetuar o login.')
            return redirect('perfil:login')
        
        usuario = authenticate(self.request, username=username, password=password)

        if usuario:
            carrinho = deepcopy(self.request.session.get('carrinho', {}))

            login(self.request, usuario)

            self.request.session['carrinho'] = carrinho
            self.request.session.save()

            next_url = self.request.GET.get('next')
            if url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
                return redirect(next_url)
            return redirect('perfil:login')
        
        messages.error(self.request, 'Usuário ou senha inválidos.')
        return redirect('perfil:login')

class Logout(View):
    def get(self, *args, **kwargs):

        carrinho = deepcopy(self.request.session.get('carrinho', {}))

        logout(self.request)

        self.request.session['carrinho'] = carrinho
        self.request.session.save()

        return redirect('produto:lista')


