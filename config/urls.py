from django.contrib import admin
from django.urls import path

from libra import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("questionnaire/", views.questionnaire, name="questionnaire"),
    path("questionnaire_details/<data_id>/", views.questionnaire_details, name="questionnaire_details"),
    path("questionnaire_details/", views.questionnaire_details_latest, name="questionnaire_details_latest"),
    path("no_details_page/", views.no_details_page, name="no_details_page"),
    path("admin/", admin.site.urls),
]
