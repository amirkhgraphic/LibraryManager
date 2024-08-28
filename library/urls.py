from django.urls import path

from library.views import AuthorCreateView

urlpatterns = [
    path('author/create/', AuthorCreateView.as_view(), name='author-create'),
]