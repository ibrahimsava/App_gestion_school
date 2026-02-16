"""
URL configuration for School_Management project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('academic/', include('academic.urls')),
    path('attendance/', include('attendance.urls')),
    path('communications/', include('communications.urls')),
    path('fees/', include('fees.urls')),
    path('librairy/', include('librairy.urls')),
    path('timetables/', include('timetables.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
