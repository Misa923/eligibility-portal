from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from requestsapp.models import (
    EligibilityRequest,
    ArchivedEligibilityRequest,
    ArchivedClientQuery,
)

class Command(BaseCommand):
    help = "Archive (audit) and delete EligibilityRequest records older than 30 days."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=30,
            help="Archive and delete requests older than this many days (default: 30).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be archived/deleted without modifying the database.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        days = options["days"]
        dry_run = options["dry_run"]
        cutoff = timezone.now() - timedelta(days=days)

        qs = EligibilityRequest.objects.select_related("requester").prefetch_related("clients").filter(created_at__lt=cutoff).order_by("created_at")
        count = qs.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS("No expired requests found."))
            return

        self.stdout.write(f"Found {count} request(s) older than {days} day(s) (cutoff: {cutoff.isoformat()}).")

        if dry_run:
            for r in qs:
                self.stdout.write(f"DRY RUN: would archive+delete request #{r.pk} (requester={r.requester}, created_at={r.created_at})")
            return

        archived_total = 0
        for r in qs:
            ar = ArchivedEligibilityRequest.objects.create(
                original_request_id=r.pk,
                requester=r.requester,
                created_at=r.created_at,
                status=r.status,
                responded_at=r.responded_at,
            )

            clients = []
            for c in r.clients.all():
                clients.append(ArchivedClientQuery(
                    archived_request=ar,
                    first_name=c.first_name,
                    middle_name=c.middle_name,
                    last_name=c.last_name,
                    dob=c.dob,
                    eligibility=c.eligibility,
                    reviewer_notes=c.reviewer_notes,
                ))
            if clients:
                ArchivedClientQuery.objects.bulk_create(clients)

            r.delete()
            archived_total += 1

        self.stdout.write(self.style.SUCCESS(f"Archived and deleted {archived_total} request(s)."))
