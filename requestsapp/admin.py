from django.contrib import admin
from .models import (
    EligibilityRequest,
    ClientQuery,
    ArchivedEligibilityRequest,
    ArchivedClientQuery,
)

class ClientQueryInline(admin.TabularInline):
    model = ClientQuery
    extra = 0

@admin.register(EligibilityRequest)
class EligibilityRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "requester", "created_at", "status", "responded_at")
    list_filter = ("status", "created_at")
    search_fields = ("requester__username", "requester__email")
    inlines = [ClientQueryInline]

@admin.register(ClientQuery)
class ClientQueryAdmin(admin.ModelAdmin):
    list_display = ("id", "request", "first_name", "middle_name", "last_name", "dob", "eligibility")
    list_filter = ("eligibility",)
    search_fields = ("first_name", "middle_name", "last_name")

class ArchivedClientQueryInline(admin.TabularInline):
    model = ArchivedClientQuery
    extra = 0

@admin.register(ArchivedEligibilityRequest)
class ArchivedEligibilityRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "original_request_id", "requester", "created_at", "status", "responded_at", "archived_at")
    list_filter = ("status", "created_at", "archived_at")
    search_fields = ("requester__username", "requester__email")
    inlines = [ArchivedClientQueryInline]

@admin.register(ArchivedClientQuery)
class ArchivedClientQueryAdmin(admin.ModelAdmin):
    list_display = ("id", "archived_request", "first_name", "middle_name", "last_name", "dob", "eligibility")
    list_filter = ("eligibility",)
    search_fields = ("first_name", "middle_name", "last_name")
