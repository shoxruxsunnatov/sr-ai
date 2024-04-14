from django.urls import path

from api.views import (
    RegisterViewAPI,
    LoginViewAPI,
    RequestGPTView
)

app_name = 'api'

urlpatterns = [
    # path('register/', RegisterViewAPI.as_view(), name='register'),
    path('login/', LoginViewAPI.as_view(), name='login'),
    path('request/', RequestGPTView.as_view(), name='request-gpt')
]