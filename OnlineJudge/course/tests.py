from django.test import TestCase

from utils.api.tests import APITestCase

from account.models import AdminType, User
from .models import Course

import copy

# Create your tests here.

DEFAULT_COURSE_DATA = {"title": "test title", "description": "test description", "students" : [], "visible" : True}

class CourseAdminAPITests(APITestCase):

    def setUp(self) :
        self.create_super_admin(login=False)
        self.create_user(username="user1", password="testtest", login=False)
        self.create_user(username="user2", password="testtest", login=False)
        self.create_user(username="user3", password="testtest", login=False)
        self.create_user(username="user4", password="testtest", login=False)
        self.create_admin(login=True)
     
        self.url = self.reverse("course_admin_api")
        self.data = copy.deepcopy(DEFAULT_COURSE_DATA)

    def test_create_course(self):
        response = self.client.post(self.url, data=self.data)
        self.assertSuccess(response)
        print(response.data["data"])
        return response

    def test_update_course(self) :
        id = self.test_create_course().data["data"]["id"]
        update_data = {"id" : id,  "title": "update title",
                       "description": "update description",
                       "students" : ["user1", "user2"]
        }
        
        data = copy.deepcopy(self.data)
        data.update(update_data)
        response = self.client.put(self.url, data=data)
        self.assertSuccess(response)
        response_data = response.data["data"]
        for k in data.keys():
            self.assertEqual(response_data[k], data[k])
        print(response.data["data"])