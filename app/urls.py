from django.urls import path, include
from app.views import CreateCheckoutSession, HomeView, SuccessView, CancelView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/<int:pk>/', CreateCheckoutSession.as_view(), name='checkout'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
]