import json

from bs4 import BeautifulSoup

from faker import Faker

from requests import get

faker = Faker()
user_agent = faker.providers[0].user_agent()

headers = ({'User-Agent': user_agent})

link = 'https://www.britishuni.com/subject-guide/subject-list'


response = get(link, headers=headers)
html_soup = BeautifulSoup(response.text, 'html.parser')
subject_container = html_soup.find_all('h5', class_="brochure-box__text")
data = [s.text for s in subject_container]

with open("university_subjects.json", "w") as write_file:
    json.dump(data, write_file)
