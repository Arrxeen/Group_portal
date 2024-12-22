# Here will be the forms for News, Calendar, Events and so on...
from django import forms
from default_pages.models import News, Event, Notification, UsefulLink


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'editor']


class EventForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Event
        fields = ['title', 'description', 'date']

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'message']

class UsefulLinkForm(forms.ModelForm):
    class Meta:
        model = UsefulLink
        fields = ['title', 'url', 'description']