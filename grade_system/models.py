from django.db import models
from auth_sys.models import CustomUser


class Teacher(models.Model):
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='teacher_profile',  
        limit_choices_to={'role__name': 'Administrator'}  
    )

    def __str__(self):
        return f"Teacher: {self.user.first_name}"


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')

    def __str__(self):
        return f"Student: {self.user.first_name}"


class Grade(models.Model):
    TYPE_GRADE = [
        ("H", "H"),
        ("H/O", "H/O"),
    ] + [(str(i), str(i)) for i in range(1, 13)]

    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='grades')
    teacher = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING,related_name='grades')
    grade = models.CharField(max_length=20,choices=TYPE_GRADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Grade: {self.grade} for {self.student.user.first_name} by {self.teacher.user.first_name}"
