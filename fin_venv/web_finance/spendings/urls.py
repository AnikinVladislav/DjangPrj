from django.urls import path
from . import views

urlpatterns = [
    path('', views.spendigs_view, name='spendings'),
]
