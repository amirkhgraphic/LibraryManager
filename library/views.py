from django.urls import reverse_lazy
from django.views import generic

from .forms import AuthorForm, BookForm
from .models import Author, Book


# Author Model Views
class AuthorCreateView(generic.CreateView):
    form_class = AuthorForm
    model = Author
    template_name = 'library/author-create.html'
    success_url = reverse_lazy('library:author-list')


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'library/author-list.html'
    context_object_name = 'authors'


class AuthorDetailView(generic.DetailView):
    model = Author
    pk_url_kwarg = 'author_id'
    template_name = 'library/author-detail.html'
    context_object_name = 'author'


# Book Model Views
class BookCreateView(generic.CreateView):
    form_class = BookForm
    model = Book
    template_name = 'library/book-create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.upload_by = self.request.user
        return super().form_valid(form)


class BookListView(generic.ListView):
    model = Book
    template_name = 'library/book-list.html'
    context_object_name = 'books'
    ordering = ('-created_at', )


class BookDetailView(generic.DetailView):
    model = Book
    pk_url_kwarg = 'book_id'
    template_name = 'library/book-detail.html'
    context_object_name = 'book'
