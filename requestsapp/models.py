from django.conf import settings
from django.db import models
from django.utils import timezone

class EligibilityRequest(models.Model):
    """A request submitted by a partner user; contains 1..N client rows."""

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending review"
        RESPONDED = "RESPONDED", "Responded"

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="eligibility_requests",
        help_text="Partner user who submitted the request.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    responded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request #{self.pk} by {self.requester} ({self.status})"

class ClientQuery(models.Model):
    """A single client row within an eligibility request."""

    class Eligibility(models.TextChoices):
        UNKNOWN = "UNKNOWN", "Not reviewed yet"
        ELIGIBLE = "ELIGIBLE", "Eligible"
        NOT_ELIGIBLE = "NOT_ELIGIBLE", "Not eligible"

    request = models.ForeignKey(EligibilityRequest, on_delete=models.CASCADE, related_name="clients")

    first_name = models.CharField(max_length=80)
    middle_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80)

    dob = models.DateField(verbose_name="Date of birth")

    eligibility = models.CharField(max_length=20, choices=Eligibility.choices, default=Eligibility.UNKNOWN)
    reviewer_notes = models.TextField(blank=True)

    @property
    def display_name(self) -> str:
        parts = [self.first_name.strip()]
        if self.middle_name.strip():
            parts.append(self.middle_name.strip())
        parts.append(self.last_name.strip())
        return " ".join([p for p in parts if p])

    def __str__(self):
        return f"{self.display_name} ({self.dob})"

class ArchivedEligibilityRequest(models.Model):
    """Audit record kept after the active request is deleted (30-day retention for active records)."""

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending review"
        RESPONDED = "RESPONDED", "Responded"

    original_request_id = models.IntegerField(help_text="Primary key of the original EligibilityRequest.")
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="archived_eligibility_requests",
    )
    created_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices)
    responded_at = models.DateTimeField(null=True, blank=True)

    archived_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Archived request #{self.original_request_id} by {self.requester}"

class ArchivedClientQuery(models.Model):
    """Audit row for each client within an archived request."""

    class Eligibility(models.TextChoices):
        UNKNOWN = "UNKNOWN", "Not reviewed yet"
        ELIGIBLE = "ELIGIBLE", "Eligible"
        NOT_ELIGIBLE = "NOT_ELIGIBLE", "Not eligible"

    archived_request = models.ForeignKey(ArchivedEligibilityRequest, on_delete=models.CASCADE, related_name="clients")

    first_name = models.CharField(max_length=80)
    middle_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80)

    dob = models.DateField(verbose_name="Date of birth")

    eligibility = models.CharField(max_length=20, choices=Eligibility.choices, default=Eligibility.UNKNOWN)
    reviewer_notes = models.TextField(blank=True)

    @property
    def display_name(self) -> str:
        parts = [self.first_name.strip()]
        if self.middle_name.strip():
            parts.append(self.middle_name.strip())
        parts.append(self.last_name.strip())
        return " ".join([p for p in parts if p])

    def __str__(self):
        return f"{self.display_name} ({self.dob})"
