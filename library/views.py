from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from .forms import AuthorForm, BookForm, ChapterForm
from .models import Author, Book, Chapter, Genre


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

    def get_queryset(self):
        queryset = super().get_queryset()
        author = self.request.GET.get('author')
        genre = self.request.GET.get('genre')
        published_date = self.request.GET.get('published_date')
        search_query = self.request.GET.get('q')

        if author:
            queryset = queryset.filter(author__id=author)
        if genre:
            queryset = queryset.filter(genres__id=genre)
        if published_date:
            queryset = queryset.filter(published_date__year=published_date)
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        context['genres'] = Genre.objects.all()
        context['search_query'] = self.request.GET.get('q')
        return context


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


class GenreListView(generic.ListView):
    model = Genre
    template_name = 'library/genre_list.html'
    context_object_name = 'genres'


class GenreDetailView(generic.DetailView):
    model = Genre
    pk_url_kwarg = 'genre_id'
    context_object_name = 'genre'
    template_name = 'library/genre_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.get_object().books.all()
        return context


@method_decorator(login_required, name='dispatch')
class MyBooksListView(generic.ListView):
    template_name = 'library/user-books.html'
    context_object_name = 'books'
    ordering = ('-created_at', )

    def get_queryset(self):
        queryset = Book.objects.filter(upload_by=self.request.user)

        author = self.request.GET.get('author')
        genre = self.request.GET.get('genre')
        published_date = self.request.GET.get('published_date')
        search_query = self.request.GET.get('q')

        if author:
            queryset = queryset.filter(author__id=author)
        if genre:
            queryset = queryset.filter(genres__id=genre)
        if published_date:
            queryset = queryset.filter(published_date__year=published_date)
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        context['genres'] = Genre.objects.all()
        context['search_query'] = self.request.GET.get('q')
        return context


@method_decorator(login_required, name='dispatch')
class MyBooksDeleteView(generic.View):
    def get_queryset(self):
        queryset = Book.objects.filter(upload_by=self.request.user)

        author = self.request.GET.get('author')
        genre = self.request.GET.get('genre')
        published_date = self.request.GET.get('published_date')
        search_query = self.request.GET.get('q')

        if not (author or genre or published_date or search_query):
            return queryset, True

        if author:
            queryset = queryset.filter(author__id=author)
        if genre:
            queryset = queryset.filter(genres__id=genre)
        if published_date:
            queryset = queryset.filter(published_date__year=published_date)
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

        return queryset, (len(queryset) == len(Book.objects.filter(upload_by=self.request.user)))

    def get(self, *args, **kwargs):
        queryset, is_all = self.get_queryset()

        context = {
            'queryset': queryset,
            'is_all': is_all,
            'search_query': self.request.GET.get('q'),
        }
        return render(self.request, 'library/user-books-delete.html', context=context)

    def post(self, request, *args, **kwargs):
        queryset, _ = self.get_queryset()
        queryset.delete()
        return redirect(reverse_lazy('library:user-books'))
