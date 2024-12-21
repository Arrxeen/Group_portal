from django.urls import path
from . import views

urlpatterns = [
    path('', views.survey_list, name='survey_list'),
    path('survey/<int:pk>/', views.survey_detail, name='survey_detail'),
    path('survey/create/', views.create_survey, name='create_survey'),
    path('survey/<int:survey_id>/add-question/', views.add_question, name='add_question'),
] 