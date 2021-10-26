import stripe
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from app.models import Product


stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSession(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs['pk']
        product = Product.objects.get(pk=product_id)
        product_stripe = stripe.Product.create(name=product.name)
        print("Product", product_stripe)

        YOUR_DOMAIN = 'http://127.0.0.1:8000/'
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': stripe.Price.create(
                            unit_amount=product.price*100,
                            currency="usd",
                            recurring={"interval": "month"},
                            product=product_stripe,
                            ),
                    'quantity': 1,
                },
            ],
            payment_method_types=['card',],
            mode='subscription',
            success_url=YOUR_DOMAIN + 'app/success/',
            cancel_url=YOUR_DOMAIN + 'cancel/',
        )

        return redirect(checkout_session.url, code=303)



class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        product = Product.objects.first()
        context = super().get_context_data(**kwargs)
        context.update({
            'product':product,
        })

        return context
    


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelView(TemplateView):
    template_name = 'cancel.html'
