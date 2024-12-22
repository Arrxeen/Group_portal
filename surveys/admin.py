from django.contrib import admin
from .models import Survey, Question, Choice, Answer

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'is_active']
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'survey', 'question_type', 'required']
    inlines = [ChoiceInline]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'survey', 'question', 'created_at']
