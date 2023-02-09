from django.urls import path
from . import views

urlpatterns = [
    path('', views.web_finance, name='web_finance'),
    path('all_spendigns/<int:id>', views.all_spendigns, name='all_spendigns'),
    path('about_us/', views.about_us, name='about_us'),
]