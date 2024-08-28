import os

from django import forms
from django.core.exceptions import ValidationError

from .models import Author, Book, Chapter


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


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = [
            'book',
            'title',
            'number',
            'content',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Enter Chapter title',
            }),
            'number': forms.NumberInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Enter Chapter number',
                'min': 1,
            }),
            'book': forms.Select(attrs={
                'class': 'form-control mb-2'
            }),
            'content': forms.FileInput(attrs={
                'class': 'form-control mb-2'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ChapterForm, self).__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(upload_by=user)

    def clean_content(self):
        content = self.cleaned_data.get('content')
        book = self.cleaned_data.get('book')

        if content and book:
            content_extension = os.path.splitext(content.name)[1].lower()
            expected_extension = f".{book.file_format.lower()}"

            if content_extension != expected_extension:
                raise ValidationError(
                    f"The uploaded content must be in {book.file_format} format."
                )

        return content
