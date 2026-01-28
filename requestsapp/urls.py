from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("requests/new/", views.request_create, name="request_create"),
    path("requests/<int:pk>/", views.request_detail, name="request_detail"),

    # staff review
    path("review/", views.review_queue, name="review_queue"),
    path("review/<int:pk>/", views.review_detail, name="review_detail"),
]
