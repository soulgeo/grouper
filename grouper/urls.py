from django.contrib import admin
from django.urls import include, path

from users.views import CustomSignupView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls')),
]
