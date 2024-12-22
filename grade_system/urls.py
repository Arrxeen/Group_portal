from django.urls import path
from .views import StudentListView, StudentDetailView, GradeEditView, GradeDeleteView

urlpatterns = [
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('grades/<int:pk>/edit/', GradeEditView.as_view(), name='grade-edit'),
    path('grades/<int:pk>/delete/', GradeDeleteView.as_view(), name='grade-delete'),
]