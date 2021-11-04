from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from stripe_monthly.views import MembershipSelectView, PaymentView, CreateCheckoutSession


urlpatterns = [
    path('', MembershipSelectView.as_view(), name='select'),
    path('payment/', PaymentView, name='payment'),
    path('checkout/', CreateCheckoutSession.as_view(), name='checkout'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)