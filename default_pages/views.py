from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from default_pages.forms import NewsForm, EventForm, NotificationForm, UsefulLinkForm
from datetime import datetime, timedelta
from .models import Event, CustomUser, News, Notification, UsefulLink
from django.utils.timezone import now

def generate_timeline_with_events(start_date, end_date):
    timeline = []
    current_date = start_date
    events = Event.objects.filter(date__range=[start_date, end_date])

    while current_date <= end_date:
        daily_events = events.filter(date=current_date)
        timeline.append({
            "day": current_date.strftime("%d"),
            "month": current_date.strftime("%b"),
            "weekday": current_date.strftime("%a"),
            "events": daily_events,
        })
        current_date += timedelta(days=1)

    return timeline

# Create your views here.
class MainView(TemplateView):
    template_name = 'default_pages/main.html'

    def get_context_data(self, **kwargs):
        today = datetime.now().date()
        thirty_days = today + timedelta(days=30)
        upcoming_birthdays = []
        for user in CustomUser.objects.all():
            if user.birth_month is not None and user.birth_day is not None:
                try:
                    birthday = datetime(today.year, user.birth_month, user.birth_day).date()
                except ValueError:
                    continue

                if today > birthday:
                    birthday = datetime(today.year + 1, user.birth_month, user.birth_day).date()

                if today <= birthday <= thirty_days:
                    upcoming_birthdays.append(user)
        

        news = News.objects.all().order_by('-created_at')[0:3]

        yesterday = now() - timedelta(days=1)
        print(yesterday)
        notif = Notification.objects.all()
        chek = Notification.objects.filter(created_at__lte=yesterday)
        if chek.exists():
            chek.delete()
            print("Notification deleted")
        else:
            print("No notifications to delete")

        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now() + timedelta(days=30)

        Event.objects.filter(date__lt=start_date-timedelta(days=1)).delete()

        timeline = generate_timeline_with_events(start_date, end_date)

        context = super().get_context_data(**kwargs)
        context['upcoming_birthdays'] = upcoming_birthdays
        context['news'] = news
        context['timeline'] = timeline
        if notif.exists():
            context['notification'] = notif[0]
        return context

class NewsListView(ListView):
    model = News
    template_name = 'default_pages/news_list.html'
    context_object_name = 'news'
    paginate_by = 6

    def get_queryset(self):
        return News.objects.order_by('-created_at')

class NewsDetailView(DetailView):
    model = News
    template_name = 'default_pages/news_detail.html'
    context_object_name = 'news_item'

    def get_queryset(self):
        return News.objects
    
class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'default_pages/add_news.html'
    permission_required = 'default_pages.can_post_news'
    success_url = reverse_lazy('news-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'default_pages/add_news.html'
    permission_required = 'default_pages.can_post_news'
    success_url = reverse_lazy('news-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_item'] = self.object
        return context

class NewsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = News
    template_name = 'default_pages/news_confirm_delete.html'
    permission_required = 'default_pages.can_post_news'
    success_url = reverse_lazy('news-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_item'] = self.object
        return context

class AboutView(TemplateView):
    template_name = "default_pages/about_page.html"
    

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'default_pages/add_event.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class EventDetailView(DetailView):
    model = Event
    template_name = 'default_pages/event_detail.html'
    context_object_name = 'event'

class EventUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'default_pages/add_event.html'
    permission_required = 'default_pages.can_modify_event'
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.object
        return context

class EventDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Event
    template_name = 'default_pages/event_confirm_delete.html'
    permission_required = 'default_pages.can_modify_event'
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.object
        return context

class NotificationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Notification
    form_class = NotificationForm
    template_name = 'default_pages/notification_form.html'
    permission_required = 'default_pages.can_create_notification'
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notification'] = self.object
        return context

    def form_valid(self, form):
        form.instance.creater = self.request.user
        return super().form_valid(form)

class NotificationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Notification
    form_class = NotificationForm
    template_name = 'default_pages/notification_form.html'
    permission_required = 'default_pages.can_modify_notification'
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notification'] = self.object
        return context

def useful_links(request):
    links = UsefulLink.objects.all()
    return render(request, 'default_pages/useful_links.html', {'links': links})

class UsefulLinkCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = UsefulLink
    form_class = UsefulLinkForm
    template_name = 'default_pages/useful_link_form.html'
    permission_required = 'default_pages.can_add_useful_link'
    success_url = reverse_lazy('useful-links')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class UsefulLinkUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = UsefulLink
    form_class = UsefulLinkForm
    template_name = 'default_pages/useful_link_form.html'
    permission_required = 'default_pages.can_edit_useful_link'
    success_url = reverse_lazy('useful-links')

class UsefulLinkDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = UsefulLink
    template_name = 'default_pages/useful_link_confirm_delete.html'
    permission_required = 'default_pages.can_delete_useful_link'
    success_url = reverse_lazy('useful-links')