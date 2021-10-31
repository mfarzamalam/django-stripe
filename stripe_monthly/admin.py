from django.contrib import admin
from stripe_monthly.models import Memebership, UserMembership, Subscription 



admin.site.register(Memebership)
admin.site.register(UserMembership)
admin.site.register(Subscription)