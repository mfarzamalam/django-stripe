from django.http import request, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Memebership, UserMembership, Subscription
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import stripe
from django.views import View



def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        user_membership = user_membership_qs.first()

    return user_membership


def get_user_subscription(request):
    user_subscription_qs = Subscription.objects.filter(user_membership=get_user_membership(request))
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
    return None


class MembershipSelectView(ListView):
    model = Memebership

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context["current_membership"] = str(current_membership.membership)

        return context

    def post(self, request, *args, **kwargs):
        selected_membership_type = request.POST.get('membership_type')

        user_membership   = get_user_membership(self.request)
        user_subscription = get_user_subscription(self.request)

        selected_membership_qs = Memebership.objects.filter(membership_type=selected_membership_type)
        if selected_membership_qs.exists():
            selected_membership = selected_membership_qs.first()

        print("user_membership", user_membership)
        print("user_subscription", user_subscription)
        print("selected_membership", selected_membership)
        print("selected_membership_type", selected_membership_type)
        print("selected_membership.membership_type", selected_membership.membership_type)


        # VALIDATION
        if user_membership.membership == selected_membership.membership_type:
            if user_subscription != None:
                messages.info(self.request, "You already subscribed to this offer. \
                    Your next payment is on {}".format('get payment date from stripe'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        
        # SESSION
        request.session['selected_membership_type'] = selected_membership.membership_type

        return HttpResponseRedirect(reverse('payment'))



def PaymentView(request):
    selected_membership = request.POST.get('membership_type')
    user_membership = Memebership.objects.filter(membership_type=selected_membership).first()
    membership_price    = request.POST.get('membership_price')

    publish_key = settings.STRIPE_SECRET_KEY    
    context = {
        'publish_key':publish_key,
        's_m':  selected_membership,
        'membership_price': membership_price,
        'price_id' : user_membership.stripe_plan_id,
    }

    return render(request, "stripe_monthly/membership_payment.html", context)


# 4000 0025 0000 3155
class CreateCheckoutSession(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = 'http://127.0.0.1:8000/'
        price_id = request.POST.get('price_id')
        retrieve_price = stripe.Price.retrieve(
              str(price_id),
        )

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': retrieve_price,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=YOUR_DOMAIN +
            'success.html?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
        print("\nSuccess url")
        print(checkout_session.success_url)
        print("\nCancel url")
        print(checkout_session.cancel_url)
        print("\nCheckout Session")
        print(checkout_session)
        return redirect(checkout_session.url, code=303)