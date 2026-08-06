from django.urls import path

from core.docs.views import DocumentationHomeView, DocumentationView

app_name = "docs"

urlpatterns = [

    path(
        "",
        DocumentationHomeView.as_view(),
        name="home",
    ),

    path(

        "<slug:slug>/",

        DocumentationView.as_view(),

        name="document",

    ),

]