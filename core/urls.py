from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views import generic

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', generic.TemplateView.as_view(template_name='home.html'), name='home'),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('library/', include(('library.urls', 'library'), namespace='library')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
