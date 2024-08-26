from django.urls import path
from django.contrib.auth import views as auth_views

from .views import ProfileUpdateView, MyLoginView, SignupView

urlpatterns = [
    path('', ProfileUpdateView.as_view(), name='profile'),
    path('signup/', SignupView.as_view(), name='sign-up'),
    path('login/', MyLoginView.as_view(), name='log-in'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='log-out'),
]
