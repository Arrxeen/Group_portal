from django.urls import path
from . import views

urlpatterns = [
    path('', views.survey_list, name='survey_list'),
    path('<int:pk>/', views.survey_detail, name='survey_detail'),
    path('<int:pk>/results/', views.survey_results, name='survey_results'),
    path('create/', views.create_survey, name='create_survey'),
    path('<int:survey_id>/add-question/', views.add_question, name='add_question'),
    path('<int:pk>/delete/', views.SurveyDeleteView.as_view(), name='survey_delete'),
]