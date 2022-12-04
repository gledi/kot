from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/home.html", context={})


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/about.html")


def contact(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/contact.html")


def privacy_policy(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/privacy_policy.html")


def jobs(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/jobs.html")
