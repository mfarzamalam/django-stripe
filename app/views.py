import stripe
from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from app.models import Product


stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSession(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = 'http://127.0.0.1:8000/'
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # TODO: replace this with the `price` of the product you want to sell
                    'price': '{{PRICE_ID}}',
                    'quantity': 1,
                },
            ],
            payment_method_types=['card',],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )

        return redirect(checkout_session.url, code=303)
