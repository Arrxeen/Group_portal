from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.all_portfolios, name='all_portfolios'),
    path('portfolio/', views.my_portfolios, name='my_portfolios'),
    path('create-portfolio/', views.create_portfolio, name='create_portfolio'),
    path('edit-portfolio/<int:pk>/', views.edit_portfolio, name='edit_portfolio'),
    path('delete-portfolio/<int:pk>/', views.delete_portfolio, name='delete_portfolio'),
]
