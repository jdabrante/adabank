from django.contrib import admin

from .models import Account, Card


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['code', 'client', 'alias', 'balance']
    list_editable = ['alias', 'balance']

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['code', 'account', 'alias', 'pin']