from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.spendigs_view, name='spendings'),
    path('add_spending', views.add_spending, name='add_spending'),
    path('edit_spending/<int:id>', views.editspending, name='edit_spending'),
    path('delete_spending/<int:id>', views.deletespending, name='delete_spending'),
]
