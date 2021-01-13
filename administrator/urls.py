from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="validation"),
    path('action/<int:id>', views.action, name="action")
]
