from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from Audience import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employ/', include('employ.urls')),
    path('job/', include('job.urls')),
    path('comment/', include('comment.urls')),
    path('account/', include('account.urls')),
    path('util/', include('util.urls')),
    path('audience/', include('Audience.urls')),
    path('', views.intro_view, name='intro_view'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
