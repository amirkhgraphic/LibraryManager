from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model, authenticate, login
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, FormView

from user.forms import SignupForm, LoginForm, ProfileForm


User = get_user_model()


class MyLoginView(LoginView):
    form_class = LoginForm
    template_name = "user/login.html"
    success_url = reverse_lazy("home")


class SignupView(FormView):
    form_class = SignupForm
    template_name = "user/signup.html"
    success_url = reverse_lazy("home")
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        raw_password = form.cleaned_data['password1']
        user = authenticate(username=username, password=raw_password)

        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Your account has been created and you are now logged in!')
        else:
            messages.error(self.request, 'There was an issue logging you in. Please try to log in manually.')

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    form_class = ProfileForm
    template_name = 'user/profile.html'

    def get_success_url(self):
        return self.request.path

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.instance = self.get_object()

        if 'avatar' in form.files:
            form.instance.avatar = form.files['avatar']

        return super().form_valid(form)
