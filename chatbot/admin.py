from django.contrib import admin
from .models import Conversation,Message,PurchasePlan,Plan

admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(PurchasePlan)
admin.site.register(Plan)

