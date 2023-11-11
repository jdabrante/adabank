from django.contrib import admin

from .models import Transaction, Commission, WhitelistedBank


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["agent", "concept", "timestamp", "amount", "kind"]


@admin.register(Commission)
class ComissionAdmin(admin.ModelAdmin):
    list_display = ["id", "kind", "range1", "range2", "range3"]
    list_editable = ["kind", "range1", "range2", "range3"]


@admin.register(WhitelistedBank)
class WhitelistedBanksAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "url", "code"]
    list_editable = ["name", "url", "code"]
