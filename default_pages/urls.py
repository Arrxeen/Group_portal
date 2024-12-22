from django.urls import path
from default_pages import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('news-list/', views.NewsListView.as_view(), name='news-list'),
    path('news-detail/<int:pk>/', views.NewsDetailView.as_view(), name='news-detail'),
    path('add-news/', views.NewsCreateView.as_view(), name='add-news'),
    path('news/<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news-edit'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news-delete'),
    path('useful-links/', views.useful_links, name='useful-links'),
    path('useful-links/add/', views.UsefulLinkCreateView.as_view(), name='useful-link-add'),
    path('useful-links/<int:pk>/edit/', views.UsefulLinkUpdateView.as_view(), name='useful-link-edit'),
    path('useful-links/<int:pk>/delete/', views.UsefulLinkDeleteView.as_view(), name='useful-link-delete'),
    path('add_event/', views.EventCreateView.as_view(), name='add-event'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('event/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event-edit'),
    path('event/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event-delete'),
    path('notification/<int:pk>/edit/', views.NotificationUpdateView.as_view(), name='notification-edit'),
    path('notification/create/', views.NotificationCreateView.as_view(), name='notification-create'),
]