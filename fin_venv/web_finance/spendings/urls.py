from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.spendigs_view, name='spendings'),
    path('add_spending', views.add_spending, name='add_spending'),
]
