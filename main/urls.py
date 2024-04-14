from django.urls import path

from main.views import (
    RegisterView,
    HomeView,
    CustomLogoutView,
    AboutView,
)

app_name = 'main'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('log-out/', CustomLogoutView.as_view(), name='log-out'),
    path('about/', AboutView.as_view(), name='about'),
    path('', HomeView.as_view(), name='home')
]