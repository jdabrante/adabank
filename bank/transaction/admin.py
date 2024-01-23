from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Transaction, Commission, WhitelistedBank


def transaction_pdf(obj):
    url = reverse("adabank:admin_transaction_pdf", args=[obj.pk])
    return mark_safe(f'<a href="{url}">PDF</a>')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["agent", "concept", "timestamp", "amount", "kind", transaction_pdf]


@admin.register(Commission)
class ComissionAdmin(admin.ModelAdmin):
    list_display = ["id", "kind", "range1", "range2", "range3"]
    list_editable = ["kind", "range1", "range2", "range3"]


@admin.register(WhitelistedBank)
class WhitelistedBanksAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "url", "code"]
    list_editable = ["name", "url", "code"]
