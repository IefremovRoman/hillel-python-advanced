from .models import Student, Group, Teacher

from django.shortcuts import render
from django.http import HttpResponse

from faker import Faker


# Help funcitons
locale = 'uk_UA'
faker = Faker(locale)

def model_pretty_viewer(query):
	return '<br/>'.join(str(q) for q in query)
	# return '<br/>'.join(map(str, raw))

# Viewers
def index(request):
	output = 'Hello, world!'
	return HttpResponse(output)

def students(request):
	student_list = Student.objects.all()
	output = model_pretty_viewer(student_list)
	return HttpResponse(output)

def generate_student(request):
	
	student = Student.objects.create(
									first_name=faker.first_name(), 
									last_name=faker.last_name(), 
									age=faker.random_int(min=0, max=100)
									)
	student_list = Student.objects.all()
	output = model_pretty_viewer(student_list)
	return HttpResponse(output)

def generate_students(request):
	if request.method == 'GET':
		
		count = request.GET.get('count', '100')
		try:
			count = int(count)
		except:
			return	HttpResponse(f'{count} not integer')
		
		if count <= 100 and count > 0:

			for i in range(int(count)):
				student = Student.objects.create(
												first_name=faker.first_name(), 
												last_name=faker.last_name(), 
												age=faker.random_int(min=17, max=22)
												)
			student_list = Student.objects.all()
			output = model_pretty_viewer(student_list)
			return HttpResponse(output)
	return	HttpResponse('Method not found')

def groups(request):
	group_list = Group.objects.all()
	output = model_pretty_viewer(group_list)
	return HttpResponse(output)

def teachers(request):
	teacher_list = Teacher.objects.all()
	output = model_pretty_viewer(teacher_list)
	return HttpResponse(output)