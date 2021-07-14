from django.http import HttpResponse
from django.shortcuts import render

from faker import Faker

from .models import Group, Student, Teacher


# Help funcitons
locale = 'uk_UA'
faker = Faker(locale)


def model_pretty_viewer(query):
    return '<br/>'.join(str(q) for q in query)
    # return '<br/>'.join(map(str, query))


# Viewers
def index(request):
    return render(request, 'index.html')


def students(request):
    student_list = Student.objects.all()
    output = model_pretty_viewer(student_list)
    return HttpResponse(output)


def generate_student(request):

    Student.objects.create(
                            first_name=faker.first_name(),
                            last_name=faker.last_name(),
                            age=faker.random_int(min=17, max=30)
                            )
    student_list = Student.objects.all()
    output = model_pretty_viewer(student_list)
    return HttpResponse(output)


def generate_students(request):
    if request.method == 'GET':

        count = request.GET.get('count', '100')
        try:
            count = int(count)
        except ValueError:
            return HttpResponse(f'{count} not integer')

        if count <= 100 and count > 0:

            for i in range(int(count)):
                Student.objects.create(
                                first_name=faker.first_name(),
                                last_name=faker.last_name(),
                                age=faker.random_int(min=17, max=30)
                                )
        student_list = Student.objects.all()
        output = model_pretty_viewer(student_list)
        return HttpResponse(output)
    return HttpResponse('Method not found')


def groups(request):
    group_list = Group.objects.all()
    output = model_pretty_viewer(group_list)
    return HttpResponse(output)


def teachers(request):
    if request.method == 'GET':

        query = Teacher.objects.all()
        first_name = request.GET.get('first_name', '')
        if first_name:
            query = query.filter(first_name=first_name)

        last_name = request.GET.get('last_name', '')
        if last_name:
            query = query.filter(last_name=last_name)

        age = request.GET.get('age', '')
        if age:
            query = query.filter(age=age)

        subject = request.GET.get('subject', '')
        if subject:
            query = query.filter(subject=subject)

        output = model_pretty_viewer(query)
        return HttpResponse(output)
    return HttpResponse('Method not found')
