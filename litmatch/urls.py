from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('predictions/', include('predictions.urls', namespace='predictions')),
    path('', TemplateView.as_view(template_name='layout.html'), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
