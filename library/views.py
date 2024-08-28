from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from .forms import AuthorForm, BookForm, ChapterForm
from .models import Author, Book, Chapter


# Author Model Views
@method_decorator(login_required, name='dispatch')
class AuthorCreateView(generic.CreateView):
    form_class = AuthorForm
    model = Author
    template_name = 'library/author-create.html'
    success_url = reverse_lazy('library:author-list')


@method_decorator(login_required, name='dispatch')
class AuthorListView(generic.ListView):
    model = Author
    template_name = 'library/author-list.html'
    context_object_name = 'authors'


@method_decorator(login_required, name='dispatch')
class AuthorDetailView(generic.DetailView):
    model = Author
    pk_url_kwarg = 'author_id'
    template_name = 'library/author-detail.html'
    context_object_name = 'author'


# Book Model Views
@method_decorator(login_required, name='dispatch')
class BookCreateView(generic.CreateView):
    form_class = BookForm
    model = Book
    template_name = 'library/book-create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.upload_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class BookListView(generic.ListView):
    model = Book
    template_name = 'library/book-list.html'
    context_object_name = 'books'
    ordering = ('-created_at', )


@method_decorator(login_required, name='dispatch')
class BookDetailView(generic.DetailView):
    model = Book
    pk_url_kwarg = 'book_id'
    template_name = 'library/book-detail.html'
    context_object_name = 'book'


@method_decorator(login_required, name='dispatch')
class BookDeleteView(generic.DeleteView):
    model = Book
    pk_url_kwarg = 'book_id'
    context_object_name = 'form'
    template_name = 'library/book-delete.html'
    success_url = reverse_lazy('library:book-list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.upload_by != self.request.user:
            raise PermissionDenied("You do not have permission to edit this book.")

        return obj


@method_decorator(login_required, name='dispatch')
class BookUpdateView(generic.UpdateView):
    model = Book
    form_class = BookForm
    pk_url_kwarg = 'book_id'
    context_object_name = 'book'
    template_name = 'library/book-update.html'
    success_url = reverse_lazy('library:book-list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.upload_by != self.request.user:
            raise PermissionDenied("You do not have permission to edit this book.")

        return obj


@method_decorator(login_required, name='dispatch')
class ChapterCreateView(generic.CreateView):
    model = Chapter
    form_class = ChapterForm
    template_name = 'library/chapter-create.html'
    success_url = reverse_lazy('library:book-list')

    def get_form_kwargs(self):
        kwargs = super(ChapterCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@method_decorator(login_required, name='dispatch')
class ChapterUpdateView(generic.UpdateView):
    model = Chapter
    form_class = ChapterForm
    pk_url_kwarg = 'chapter_id'
    context_object_name = 'chapter'
    template_name = 'library/chapter-update.html'
    success_url = reverse_lazy('library:book-list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.book.upload_by != self.request.user:
            raise PermissionDenied("You do not have permission to edit this book.")

        return obj

    def get_form_kwargs(self):
        kwargs = super(ChapterUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@method_decorator(login_required, name='dispatch')
class ChapterDeleteView(generic.DeleteView):
    model = Chapter
    template_name = 'library/chapter-delete.html'
    success_url = reverse_lazy('library:book-list')
    pk_url_kwarg = 'chapter_id'
    context_object_name = 'form'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.book.upload_by != self.request.user:
            raise PermissionDenied("You do not have permission to edit this book.")

        return obj


@method_decorator(login_required, name='dispatch')
class ChapterDetailView(generic.DetailView):
    model = Chapter
    pk_url_kwarg = 'chapter_id'
    template_name = 'library/chapter-detail.html'
    context_object_name = 'chapter'
