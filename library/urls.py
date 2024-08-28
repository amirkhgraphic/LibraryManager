from django.urls import path

from library.views import AuthorCreateView, AuthorListView, AuthorDetailView, BookCreateView, BookListView, BookDetailView

urlpatterns = [
    # Author Model Urls
    path('author/create/', AuthorCreateView.as_view(), name='author-create'),
    path('author/', AuthorListView.as_view(), name='author-list'),
    path('author/<int:author_id>', AuthorDetailView.as_view(), name='author-detail'),

    # Book Model Urls
    path('book/create/', BookCreateView.as_view(), name='book-create'),
    path('book/', BookListView.as_view(), name='book-list'),
    path('book/<int:book_id>', BookDetailView.as_view(), name='book-detail'),
]
