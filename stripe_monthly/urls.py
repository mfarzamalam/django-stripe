from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from stripe_monthly.views import HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='s_home'),
]  + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)