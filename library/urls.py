from django.urls import path

from library.views import AuthorCreateView, AuthorListView, AuthorDetailView

urlpatterns = [
    # Author Model Urls
    path('author/create/', AuthorCreateView.as_view(), name='author-create'),
    path('author/', AuthorListView.as_view(), name='author-list'),
    path('author/<int:author_id>', AuthorDetailView.as_view(), name='author-detail'),
]
