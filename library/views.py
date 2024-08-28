from django.urls import reverse_lazy
from django.views import generic

from .forms import AuthorForm
from .models import Author


class AuthorCreateView(generic.CreateView):
    form_class = AuthorForm
    model = Author
    template_name = 'library/author-create.html'
    success_url = reverse_lazy('home')
