from django import http
from django.contrib.auth.models import User
from django.db import models
from django.http import request, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from .models import Memebership, UserMembership, Subscription
from django.contrib import messages
from django.urls import reverse


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