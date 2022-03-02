from django.conf.urls import url, include
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import RedirectView

urlpatterns = [
    url("^$", RedirectView.as_view(pattern_name="register")),
    url(
        "^register/",
        CreateView.as_view(
            template_name="register.html", form_class=UserCreationForm, success_url="/"
        ),
        name="register",
    ),
    url("^accounts/", include("django.contrib.auth.urls")),
    # rest of your URLs as normal
]
