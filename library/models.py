from datetime import date

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Author(models.Model):
    avatar = models.ImageField(upload_to='author/', default='default/avatar.png')
    first_name = models.CharField(max_length=63)
    middle_name = models.CharField(max_length=63, blank=True, default='')
    last_name = models.CharField(max_length=63)
    bio = models.TextField(blank=True, default='')
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_alive(self):
        return self.death_date is None

    @property
    def age(self):
        if not self.birth_date:
            return None

        end_date = self.death_date if self.death_date else date.today()
        return (end_date.year - self.birth_date.year) - (
                (end_date.month, end_date.day) < (self.birth_date.month, self.birth_date.day)
        )

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'


class Genre(models.Model):
    name = models.CharField(max_length=63, unique=True)
    thumbnail = models.ImageField(upload_to='genre/', default='default/genre.png')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    class BookFileFormat(models.TextChoices):
        # EBook Formats
        PDF = 'PDF', 'Portable Document Format (PDF)'
        EPUB = 'EPUB', 'Electronic Publication (EPUB)'
        MOBI = 'MOBI', 'Mobipocket (MOBI)'
        AZW = 'AZW', 'Amazon Word (AZW)'
        TXT = 'TXT', 'Text File (TXT)'
        DOCX = 'DOCX', 'Word Document (DOCX)'
        RTF = 'RTF', 'Rich Text Format (RTF)'
        HTML = 'HTML', 'HTML (HTML)'
        # Audio Formats
        MP3 = 'MP3', 'MP3 Audio'
        AAC = 'AAC', 'AAC Audio'
        M4A = 'M4A', 'M4A Audio'
        WAV = 'WAV', 'WAV Audio'
        FLAC = 'FLAC', 'FLAC Audio'
        OGG = 'OGG', 'OGG Audio'
        WMA = 'WMA', 'WMA Audio'

    class BookType(models.TextChoices):
        EBOOK = "EBOOK", 'E-Book'
        AUDIOBOOK = "AUDIOBOOK", 'Audio Book'

    title = models.CharField(max_length=127)
    description = models.TextField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='book/cover/')
    published_date = models.DateField(null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name='books')
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    upload_by = models.ForeignKey(User, on_delete=models.CASCADE)
    book_type = models.CharField(max_length=10, choices=BookType.choices, default=BookType.EBOOK)
    file_format = models.CharField(max_length=4, choices=BookFileFormat.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def rate(self):
        return self.review_set.aggregate(average=models.Avg('rate'))['average'] or 0.0

    @staticmethod
    def user_audio_books(user: User):
        return user.book_set.filter(book_type=Book.BookType.AUDIOBOOK).all()

    @staticmethod
    def user_e_books(user: User):
        return user.book_set.filter(book_type=Book.BookType.EBOOK).all()

    def get_chapters(self):
        return self.chapter_set.order_by('number')

    def get_reviews(self):
        return self.review_set.order_by('-created_at')

    def __str__(self):
        return f'"{self.title}"'


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=127, null=True, blank=True)
    number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), ]
    )
    content = models.FileField(upload_to='book/chapters/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'number')

    def __str__(self):
        return f'{self.book} chapter#{self.number} "{self.title}"'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    @property
    def likes(self):
        return self.like_set.count()

    def __str__(self):
        return f'{self.user} rated {self.rate}/5 on {self.book}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')

    def __str__(self):
        return f'{self.user} liked comment#{self.review.id}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f'{self.user} added {self.book}'


class ReadingProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    percentage = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_complete(self):
        return self.percentage == 100

    @staticmethod
    def user_reading_progress(user: User):
        return user.readingprogress_set.filter(percentage__lt=100)

    class Meta:
        unique_together = ('user', 'book', 'chapter')

    def __str__(self):
        return f'{self.user} reads {self.percentage}% of {self.chapter}'
