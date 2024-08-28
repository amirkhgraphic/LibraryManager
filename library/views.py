from django.urls import reverse_lazy
from django.views import generic

from .forms import AuthorForm
from .models import Author


# Author Model Views
class AuthorCreateView(generic.CreateView):
    form_class = AuthorForm
    model = Author
    template_name = 'library/author-create.html'
    success_url = reverse_lazy('home')


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'library/author-list.html'
    context_object_name = 'authors'


class AuthorDetailView(generic.DetailView):
    model = Author
    pk_url_kwarg = 'author_id'
    template_name = 'library/author-detail.html'
    context_object_name = 'author'
