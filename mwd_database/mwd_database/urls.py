
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from mwd_database import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/admin/', permanent=False)),  # Перенаправление на админку
]

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))