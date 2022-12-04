from django.urls import path

from . import views

# app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("about-us/", views.about, name="about"),
    path("contact-us/", views.contact, name="contact"),
    path("privacy-policy/", views.privacy_policy, name="privacy"),
    path("work-for-us/", views.jobs, name="jobs"),
]