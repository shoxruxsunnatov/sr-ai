from openai import OpenAI
from datetime import timedelta, timezone, datetime

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

from main.models import RequestLog


class RegisterViewAPI(View):

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, req, **kwargs):
        return super().dispatch(req, **kwargs)
    
    def post(self, req, *args, **kwargs):

        username = req.POST.get('username', '').strip().lower()
        password = req.POST.get('password', '').strip()
        fullname = req.POST.get('fullname', '')
        password_repeat = req.POST.get('password_repeat')

        errors = []

        if len(password) < 8:
            errors.append('password')
        
        if password != password_repeat:
            errors.append('password-repeat')

        if not 2 < len(fullname) < 50:
            errors.append('fullname')
        
        if not 2 < len(username) < 30 or User.objects.filter(username=username).first():
            errors.append('username')

        if errors:
            return JsonResponse({'errors': errors}, safe=False)
        else:
            user = User.objects.create(
                username=username,
                is_staff=True
            )
            user.set_password(password)
            user.save()
            login(req, user)

            return JsonResponse({'message': 'success', 'errors': errors})                


class LoginViewAPI(View):

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, req, **kwargs):
        return super().dispatch(req, **kwargs)
    
    def post(self, req, *args, **kwargs):

        username = req.POST.get('username', '').strip().lower()
        password = req.POST.get('password', '')
        
        user = authenticate(username=username, password=password)
        if user:
            login(req, user)

            return JsonResponse({'message': 'success'})
                
        return JsonResponse({'message': 'failed'})


class RequestGPTView(LoginRequiredMixin, View):

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, req, **kwargs):
        return super().dispatch(req, **kwargs)

    def post(self, req, *args, **kwargs):

        data = {
            'message': 'failed',
            'errors': [],
            'trial': req.user.trial
        }

        if req.user.trial > 0:
            text = req.POST.get('text', '').strip()

            if len(text) > 4:

                req.user.trial -= 1
                req.user.save()

                client = OpenAI()
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": 'You are grammar mastermind. '
                        },
                        {
                            "role": "system",
                            "content": "You will be given grammatically wrong text. Change its words to make it correct. Count mistakes."
                        },
                        {
                            "role": "system",
                            "content": 'Never forget to wrap words with "<b>" tag which you have changed.'
                        },
                        {
                            "role": "system",
                            "content": 'Respond in JSON format: {"text": "", "mistakes": 0}'
                        },
                        {
                            "role": "user",
                            "content": text
                        }

                    ],
                    model="gpt-3.5-turbo-0125",
                    temperature=0,
                    top_p=0
                )

                data.update(
                    {
                        'message': 'success',
                        'text': chat_completion.choices[0].message.content,
                        'trial': req.user.trial
                    }
                )

                RequestLog(user=req.user, request=text, response=chat_completion.choices[0].message.content).save()

            else:
                data['errors'].append('min-length')

        else:
            data['errors'].append('limit-reached')

        return JsonResponse(data, safe=False)
