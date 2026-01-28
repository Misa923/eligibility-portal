from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .decorators import staff_required
from .forms import PartnerSignUpForm, PartnerLoginForm, ClientQueryFormSet, ReviewClientQueryFormSet
from .models import EligibilityRequest, ClientQuery

def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = PartnerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created. You can submit eligibility requests now.")
            return redirect("dashboard")
    else:
        form = PartnerSignUpForm()
    return render(request, "requestsapp/signup.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    view = LoginView.as_view(
        template_name="requestsapp/login.html",
        authentication_form=PartnerLoginForm
    )
    return view(request)

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    qs = EligibilityRequest.objects.filter(requester=request.user).order_by("-created_at")
    return render(request, "requestsapp/dashboard.html", {"requests": qs})

@login_required
def request_create(request):
    req_obj = EligibilityRequest(requester=request.user)
    if request.method == "POST":
        formset = ClientQueryFormSet(request.POST, instance=req_obj, prefix='clients')
        if formset.is_valid():
            req_obj.save()
            formset.save()

            # notify admin
            subject = f"New eligibility request #{req_obj.pk}"
            body_lines = [
                f"Requester: {request.user.username} ({request.user.email})",
                f"Request ID: {req_obj.pk}",
                f"Submitted: {timezone.localtime(req_obj.created_at).strftime('%Y-%m-%d %H:%M')}",
                "",
                "Clients:",
            ]
            for idx, c in enumerate(req_obj.clients.all(), start=1):
                body_lines.append(f"{idx}. {c.display_name} - DOB: {c.dob}")
            body_lines.append("")
            body_lines.append("Log in to the portal to review and respond.")
            send_mail(subject, "\n".join(body_lines), settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_NOTIFY_EMAIL])

            messages.success(request, f"Request #{req_obj.pk} submitted. You'll be emailed when it is reviewed.")
            return redirect("request_detail", pk=req_obj.pk)
    else:
        formset = ClientQueryFormSet(instance=req_obj, prefix='clients')

    return render(request, "requestsapp/request_create.html", {"formset": formset})

@login_required
def request_detail(request, pk: int):
    req_obj = get_object_or_404(EligibilityRequest, pk=pk, requester=request.user)
    return render(request, "requestsapp/request_detail.html", {"req": req_obj})

@staff_required
def review_queue(request):
    qs = EligibilityRequest.objects.select_related("requester").filter(status=EligibilityRequest.Status.PENDING).order_by("created_at")
    return render(request, "requestsapp/review_queue.html", {"requests": qs})

@staff_required
def review_detail(request, pk: int):
    req_obj = get_object_or_404(EligibilityRequest.objects.select_related("requester"), pk=pk)

    if request.method == "POST":
        formset = ReviewClientQueryFormSet(request.POST, instance=req_obj, prefix='clients')
        if formset.is_valid():
            formset.save()
            req_obj.status = EligibilityRequest.Status.RESPONDED
            req_obj.responded_at = timezone.now()
            req_obj.save(update_fields=["status", "responded_at"])

            # Email the partner that results are available
            partner = req_obj.requester
            if partner.email:
                subject = f"Eligibility results available for request #{req_obj.pk}"
                lines = [
                    f"Your eligibility request #{req_obj.pk} has been reviewed.",
                    "Log in to the portal to view the results.",
                    "",
                    "Summary:",
                ]
                for idx, c in enumerate(req_obj.clients.all(), start=1):
                    lines.append(f"{idx}. {c.display_name} (DOB {c.dob}) -> {c.get_eligibility_display()}")
                send_mail(subject, "\n".join(lines), settings.DEFAULT_FROM_EMAIL, [partner.email])

            messages.success(request, f"Request #{req_obj.pk} marked responded and partner notified.")
            return redirect("review_queue")
    else:
        formset = ReviewClientQueryFormSet(instance=req_obj, prefix='clients')

    return render(request, "requestsapp/review_detail.html", {"req": req_obj, "formset": formset})
