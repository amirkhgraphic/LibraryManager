from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Author, Genre, Book, Chapter, Review, Like, Favorite, ReadingProgress

User = get_user_model()


class BookInline(admin.StackedInline):
    model = Book
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('render_avatar', 'first_name', 'middle_name', 'last_name', 'birth_date', 'death_date', 'age',
                    'is_alive', 'created_at')
    list_filter = (
        ('created_at', admin.DateFieldListFilter),
        ('birth_date', admin.DateFieldListFilter),
        ('death_date', admin.DateFieldListFilter),
    )
    readonly_fields = ('render_avatar', 'created_at', 'is_alive', 'age')
    search_fields = ('first_name', 'middle_name', 'last_name')
    ordering = ('-created_at', )
    inlines = (BookInline, )

    fieldsets = [
        (_('Personal Information'), {
            'fields': [
                'render_avatar',
                'avatar',
                'first_name',
                'middle_name',
                'last_name',
                'bio',
                'is_alive',
                'age',
            ],
        }),
        (_('Important Dates'), {
            'fields': [
                'birth_date',
                'death_date',
                'created_at',
            ],
        }),
    ]

    def render_avatar(self, obj):
        return format_html(
            f'<img src="{obj.avatar.url}" width="50px" style="max-height: 50px; border-radius: 50%; " />'
        )
    render_avatar.short_description = _('Profile Image')

    def is_alive(self, obj):
        return obj.is_alive
    is_alive.short_description = _('Is Alive')
    is_alive.boolean = True


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('render_thumbnail', 'name', 'created_at')
    readonly_fields = ('render_thumbnail', 'created_at')
    search_fields = ('name', )
    ordering = ('-created_at',)
    fields = ('thumbnail', 'render_thumbnail', 'name', 'created_at')

    def render_thumbnail(self, obj):
        return format_html(
            f'<img src="{obj.thumbnail.url}" width="50px" height="50px" style="border-radius: 50%;" />'
        )
    render_thumbnail.short_description = _('Thumbnail')


class ChapterInline(admin.StackedInline):
    model = Chapter
    extra = 0
    readonly_fields = ('created_at', )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('render_cover', 'title', 'author', 'published_date', 'book_type', 'file_format', 'rate',
                    'upload_by', 'created_at')
    list_filter = (
        ('published_date', admin.DateFieldListFilter),
        'author',
        'book_type',
        'file_format',
        'upload_by',
    )
    readonly_fields = ('render_cover', 'created_at', 'rate')
    search_fields = ('title', 'description')
    ordering = ('-published_date', )
    inlines = (ChapterInline, )

    def render_cover(self, obj):
        return format_html(
            f'<img src="{obj.cover_image.url}" width="30px" height="50px" />'
        )
    render_cover.short_description = _('Cover Image')


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'book_link', 'number', 'title', 'created_at')
    list_filter = ('book', 'number')
    readonly_fields = ('created_at', 'book_link')
    search_fields = ('title', )
    ordering = ('-book', '-number')

    def book_link(self, instance):
        url = reverse('admin:library_book_change', args=[instance.pk])
        return format_html(f'<a href="{url}">{instance.book}</a>')
    book_link.short_description = _('Book')


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user_link', 'book_link', 'rate', 'likes', 'comment_preview', 'created_at')
    list_filter = ('user', 'book', 'rate')
    readonly_fields = ('user_link', 'book_link', 'comment_preview', 'likes', 'created_at')
    search_fields = ('comment',)
    inlines = (LikeInline, )

    def user_link(self, instance):
        url = reverse('admin:user_user_change', args=[instance.pk])
        return format_html(f'<a href="{url}">{instance.user}</a>')
    user_link.short_description = _('User')

    def book_link(self, instance):
        url = reverse('admin:library_book_change', args=[instance.pk])
        return format_html(f'<a href="{url}">{instance.book}</a>')
    book_link.short_description = _('Book')

    def comment_preview(self, obj):
        return obj.comment[:15] + '...' if (obj.comment and len(obj.comment) > 15) else obj.comment
    comment_preview.short_description = _('Comment Preview')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user_link', 'review_link', 'created_at')
    list_filter = ('user', 'review')
    readonly_fields = ('user_link', 'review_link')

    def review_link(self, instance):
        url = reverse('admin:library_review_change', args=[instance.pk])
        return format_html('<a href="{}">{}</a>', url, instance.review)
    review_link.short_description = _('Review')

    def user_link(self, instance):
        url = reverse('admin:user_user_change', args=[instance.pk])
        return format_html(f'<a href="{url}">{instance.user}</a>')
    user_link.short_description = _('User')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user_link', 'book_link', 'created_at')
    readonly_fields = ('user_link', 'book_link', 'created_at')
    list_filter = ('user', 'book')

    def user_link(self, instance):
        url = reverse('admin:user_user_change', args=[instance.pk])
        return format_html(f'<a href="{url}">{instance.user}</a>')
    user_link.short_description = _('User')

    def book_link(self, instance):
        url = reverse('admin:library_book_change', args=[instance.pk])
        return format_html(f'<a href="{url}">{instance.book}</a>')
    book_link.short_description = _('Book')


@admin.register(ReadingProgress)
class ReadingProgressAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user_link', 'book_link', 'chapter_link', 'percentage', 'is_complete', 'created_at')
    readonly_fields = ('user_link', 'book_link', 'chapter_link', 'is_complete', 'created_at')
    list_filter = ('user', 'book', 'chapter')

    def is_complete(self, obj):
        return obj.is_complete
    is_complete.boolean = True

    def user_link(self, instance):
        url = reverse('admin:user_user_change', args=[instance.pk])
        return format_html(f'<a href="{url}">{instance.user}</a>')
    user_link.short_description = _('User')

    def book_link(self, instance):
        url = reverse('admin:library_book_change', args=[instance.pk])
        return format_html(f'<a href="{url}">{instance.book}</a>')
    book_link.short_description = _('Book')

    def chapter_link(self, instance):
        url = reverse('admin:library_chapter_change', args=[instance.pk])
        return format_html(f'<a href="{url}">#{instance.chapter.number} {instance.chapter.title}</a>')
    chapter_link.short_description = _('Chapter')

