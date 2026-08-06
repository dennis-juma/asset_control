from django.urls import path

from .views import (
    UIHomeView,
    DataGridDemoView,
)

app_name = "playground"

urlpatterns = [

    path(
        "",
        UIHomeView.as_view(),
        name="index",
    ),

    path(
        "datagrid/",
        DataGridDemoView.as_view(),
        name="datagrid",
    ),

]

