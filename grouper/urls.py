from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from users.views import CustomSignupView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
    path('accounts/', include('allauth.urls')),
    path('_nested_admin/', include('nested_admin.urls')),
    path('', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
