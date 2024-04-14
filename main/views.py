from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin



class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

class CustomLogoutView(LogoutView):
    next_page = 'main:register'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'
    

    def get(self, req, *args, **kwargs):
        self.user = req.user

        return super().get(req, *args, **kwargs)


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        return context
    

class RegisterView(TemplateView):
    template_name = 'register.html'

    def post(self, req, *args, **kwargs):

        username = req.POST.get('username', '').strip().lower()
        password = req.POST.get('password')
        action = req.POST.get('action')

        self.context = {
            'username': username,
            'password': password
        }
        
        if action == 'login':
            user = authenticate(username=username, password=password)
            if user:
                login(req, user)

                return redirect('main:home')
            
        elif action == 'register' and not action:
            fullname = req.POST.get('fullname', '')
            password_repeat = req.POST.get('password-repeat')

            self.context['fullname'] = fullname
            self.context['password_repeat'] = password_repeat
            self.context.update({
                'fullname': fullname,
                'password_repeat': password_repeat,
                'action': 'register'
            })

            if password_repeat != password:
                self.context['password_repeat_error'] = 'is-invalid'
                return super().get(req, *args, **kwargs)
            
            if User.objects.filter(username=username).first():
                self.context['username_error'] = 'is-invalid'
                return super().get(req, *args, **kwargs)
                
        return redirect('main:register')


    def get(self, req, *args, **kwargs):

        if req.user.is_authenticated:
            
            return redirect('main:home')
        
        return super().get(req, *args, **kwargs)


class AboutView(TemplateView):
    template_name = 'about.html'
