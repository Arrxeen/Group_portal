from django.urls import path
from . import views

app_name = 'voting'

urlpatterns = [
    path('', views.voting_list, name='list'),
    path('create/', views.voting_create, name='create'),
    path('<int:pk>/', views.voting_detail, name='detail'),
    path('<int:pk>/delete/', views.VotingDeleteView.as_view(), name='delete'),
] 