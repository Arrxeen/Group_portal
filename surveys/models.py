from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Survey(models.Model):
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        permissions = [
            ('can_create_survey', 'Can create survey'),
            ('can_view_survey_results', 'Can view survey results'),
            ('can_delete_survey', 'Can delete survey'),
        ]

    def __str__(self):
        return self.title

class Question(models.Model):
    TYPES = (
        ('text', 'Текстовый ответ'),
        ('single', 'Один вариант'),
        ('multiple', 'Множественный выбор'),
    )
    
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField('Текст вопроса')
    question_type = models.CharField('Тип вопроса', max_length=8, choices=TYPES)
    required = models.BooleanField('Обязательный вопрос', default=True)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField('Вариант ответа', max_length=200)

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'

    def __str__(self):
        return self.text

class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text_answer = models.TextField('Текстовый ответ', blank=True, null=True)
    choice_answer = models.ManyToManyField(Choice, blank=True)
    created_at = models.DateTimeField('Дата ответа', auto_now_add=True)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'