from django.urls import path

from library import views

urlpatterns = [
    # Author Model Urls
    path('author/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('author/', views.AuthorListView.as_view(), name='author-list'),
    path('author/<int:author_id>/', views.AuthorDetailView.as_view(), name='author-detail'),

    # Book Model Urls
    path('book/create/', views.BookCreateView.as_view(), name='book-create'),
    path('book/', views.BookListView.as_view(), name='book-list'),
    path('book/<int:book_id>/', views.BookDetailView.as_view(), name='book-detail'),
    path('book/update/<int:book_id>/', views.BookUpdateView.as_view(), name='book-update'),
    path('book/delete/<int:book_id>/', views.BookDeleteView.as_view(), name='book-delete'),

    # Chapter Model Urls
    path('chapter/create/', views.ChapterCreateView.as_view(), name='chapter-create'),
    path('chapter/update/<int:chapter_id>', views.ChapterUpdateView.as_view(), name='chapter-update'),
    path('chapter/delete/<int:chapter_id>', views.ChapterDeleteView.as_view(), name='chapter-delete'),
    path('chapter/<int:chapter_id>', views.ChapterDetailView.as_view(), name='chapter-detail'),

    # Genre Model Urls
    path('genre/', views.GenreListView.as_view(), name='genre-list'),
    path('genre/<int:genre_id>/', views.GenreDetailView.as_view(), name='genre-detail'),

    path('my-books/', views.MyBooksListView.as_view(), name='user-books'),
]
