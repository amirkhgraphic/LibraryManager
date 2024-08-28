from django import forms

from .models import Author, Book


class DateInput(forms.DateInput):
    input_type = 'date'


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = [
            'avatar',
            'first_name',
            'middle_name',
            'last_name',
            'bio',
            'birth_date',
            'death_date',
        ]
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'upload author profile picture (optional)'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Enter author first name'
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Enter author middle name (optional)'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Enter author last name'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Enter author biography (optional)'
            }),
            'birth_date': DateInput(attrs={
                'class': 'form-control mb-2'
            }),
            'death_date': DateInput(attrs={
                'class': 'form-control mb-2'
            }),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'cover_image',
            'title',
            'description',
            'published_date',
            'author',
            'book_type',
            'file_format',
            'genres',
        ]
        widgets = {
            'cover_image': forms.ClearableFileInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Upload cover image (optional)'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Enter book title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Enter book description (optional)'
            }),
            'published_date': DateInput(attrs={
                'class': 'form-control mb-2'
            }),
            'author': forms.Select(attrs={
                'class': 'form-control mb-2'
            }),
            'book_type': forms.Select(attrs={
                'class': 'form-control mb-2'
            }),
            'file_format': forms.Select(attrs={
                'class': 'form-control mb-2'
            }),
            'genres': forms.SelectMultiple(attrs={
                'class': 'form-control mb-2'
            }),
        }
