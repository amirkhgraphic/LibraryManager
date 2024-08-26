from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html

from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = ('user_link', 'render_avatar', 'created_at', 'last_login', 'is_active', 'is_staff')
    readonly_fields = ('render_avatar', 'created_at', 'updated_at', 'last_login')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    fieldsets = (
        (_('basic'), {'fields': (('render_avatar', 'avatar'), 'username', 'first_name', 'last_name', 'email')}),
        (_('Important dates'), {'fields': ('created_at', 'updated_at', 'last_login')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active')}),
    )
    list_filter = (
        'is_active',
        ('created_at', admin.DateFieldListFilter),
        ('updated_at', admin.DateFieldListFilter)
    )

    add_fieldsets = (
        ('Required Fields', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Optional Fields', {
            'classes': ('wide',),
            'fields': ('avatar', 'is_active', 'is_staff'),
        }),
    )

    def user_link(self, obj):
        url = reverse("admin:user_user_change", args=[obj.id])
        return format_html(
            '<a href="{}">{}</a>', url, obj
        )

    user_link.short_description = 'User'

    def render_avatar(self, obj):
        return format_html(
            f'<img src="{obj.avatar.url}" width="50px" style="max-height: 50px; border-radius: 50%; " />'
        )

    render_avatar.short_description = 'Profile Image'

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
        super().delete_queryset(request, queryset)
