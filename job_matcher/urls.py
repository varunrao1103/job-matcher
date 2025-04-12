from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import index  # Import the index view from users app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),  # Home page
    path('users/', include('users.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
