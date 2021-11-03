from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from stripe_monthly.views import MembershipSelectView


urlpatterns = [
    path('', MembershipSelectView.as_view(), name='select'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)