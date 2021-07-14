from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)
    age = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id} \
                    {self.first_name} \
                    {self.last_name} \
                    {self.age}'


class Group(models.Model):
    student_id = models.CharField(max_length=24)
    teacher_id = models.CharField(max_length=24)

    def __str__(self):
        return f'{self.id} {self.student_id} {self.teacher_id}'


class Teacher(models.Model):
    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)
    age = models.IntegerField(default=0)
    subject = models.CharField(max_length=24)

    def __str__(self):
        return f'{self.id} \
                    {self.first_name} \
                    {self.last_name} \
                    {self.age} \
                    {self.subject}'
