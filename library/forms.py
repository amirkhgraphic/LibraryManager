from django import forms

from .models import Author


class DateInput(forms.DateInput):
    input_type = 'date'


class AuthorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['avatar'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['avatar'].widget.attrs['placeholder'] = 'upload author profile picture (optional)'

        self.fields['first_name'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter author first name'

        self.fields['middle_name'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['middle_name'].widget.attrs['placeholder'] = 'Enter author middle name (optional)'

        self.fields['last_name'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter author last name'

        self.fields['bio'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['bio'].widget.attrs['placeholder'] = 'Enter author biography (optional)'

        self.fields['birth_date'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['death_date'].widget.attrs['class'] = 'form-control mb-2'

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
            'birth_date': DateInput(),
            'death_date': DateInput(),
        }
