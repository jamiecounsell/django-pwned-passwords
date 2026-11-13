from django.contrib.auth.forms import UserCreationForm
from django.urls import include, path
from django.views.generic import RedirectView
from django.views.generic.edit import CreateView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="register")),
    path(
        "register/",
        CreateView.as_view(
            template_name="register.html", form_class=UserCreationForm, success_url="/"
        ),
        name="register",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    # rest of your URLs as normal
]
