import json
from random import choice

from faker import Faker

from django.core.management.base import BaseCommand
from students.models import Teacher


faker = Faker()
json_file = 'students/management/commands/university_subjects.json'


class Command(BaseCommand):
    help = 'Generate teachers'

    def add_arguments(self, parser):
        parser.add_argument('total', nargs='?', type=int)

    def handle(self, *args, **kwargs):
        # count = kwargs.get('total', 100)
        count = kwargs.get('total') if kwargs.get('total') else 100

        with open(json_file, 'r') as file:

            subjects = json.load(file)

        for i in range(count):
            teacher = Teacher.objects.create(
                                        first_name=faker.first_name(),
                                        last_name=faker.last_name(),
                                        age=faker.random_int(min=30, max=100),
                                        subject=choice(subjects)
                                        )

        message = f'{count} teacher(s) successfully created!'
        self.stdout.write(self.style.SUCCESS(message)
