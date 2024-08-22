import os
import shutil
from django.test import TestCase, Client
from users.models import User
import json

JSON = 'application/json'

# Create your tests here.

class TestLogin(TestCase):
    def setUp(self):
        self.c = Client()
        user = User(firstName="test", lastName="test", email="test@gmail.com", username="test", folderName="test", password="test")
        user.save()
    
    def tearDown(self):
        # Brisanje testnog foldera nakon testa
        if os.path.exists("media"):
            shutil.rmtree("media")

    def test_login_successful(self):
        user = {
            "username":"test",
            "password":"test"
        }
        response = self.c.post('/login', json.dumps(user), HTTP_AUTHORIZATION='', content_type=JSON)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SUCCESS')

    def test_login_false(self):
        user = {
            "username":"test1",
            "password":"test"
        }
        response = self.c.post('/login', json.dumps(user), HTTP_AUTHORIZATION='', content_type=JSON)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'USER_NOT_FOUND')

class TestRegistration(TestCase):
    def setUp(self):
        self.c = Client()
    
    def tearDown(self):
        # Brisanje testnog foldera nakon testa
        if os.path.exists("media"):
            shutil.rmtree("media")
    
    def test_registration_successiful(self):
        user = {
            "firstName": "test",
            "lastName": "test",
            "password": "test",
            "email": "test@gmail.com"
        }

        response = self.c.post('/registration', json.dumps(user), HTTP_AUTHORIZATION='', content_type=JSON)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SUCCESS')

        user = {
            "username":"test",
            "password":"test"
        }
        response = self.c.post('/login', json.dumps(user), HTTP_AUTHORIZATION='', content_type=JSON)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SUCCESS')
    
    def test_registration_false(self):
        user = {
            "firstName": "test",
            "lastName": "test",
            "password": "test",
            "email": "test@gmail.com"
        }

        response = self.c.post('/registration', json.dumps(user), HTTP_AUTHORIZATION='', content_type=JSON)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SUCCESS')

        response1 = self.c.post('/registration', json.dumps(user), HTTP_AUTHORIZATION='', content_type=JSON)

        self.assertEqual(response1.status_code, 200)
        self.assertContains(response1, 'NOT_SAVE_MAIL')

class TestUser(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User(firstName="test", lastName="test", email="test@gmail.com", username="test", folderName="test", password="test")
        self.user.save()
    
    def tearDown(self):
        # Brisanje testnog foldera nakon testa
        if os.path.exists("media"):
            shutil.rmtree("media")

    def test_filter_findOne(self):
        response = self.c.get('/user-filter/test', HTTP_AUTHORIZATION='', content_type=JSON)
        
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data), 1)

    def test_filter_notFinde(self):
        response = self.c.get('/user-filter/abc', HTTP_AUTHORIZATION='', content_type=JSON)
        
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data), 0)

    def test_updateUser_success(self):
        update = {
            "id": self.user.id,
            "username": "petar"
        }

        response = self.c.put('/user-edit', json.dumps(update), HTTP_AUTHORIZATION='', content_type=JSON)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'petar')
    
    def test_updateUserWithUserIdNotCorectly_feiled(self):
        update = {
            "id": 1999999,
            "username": "petar"
        }


        response = self.c.put('/user-edit', json.dumps(update), HTTP_AUTHORIZATION='', content_type=JSON)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'USER_NOT_FOUND')

    def test_updateUserWithUserIdIsCorectlyButNotDataCorectly_feiled(self):
        update = {
            "id": self.user.id,
        }

        response = self.c.put('/user-edit', json.dumps(update), HTTP_AUTHORIZATION='', content_type=JSON)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'NOT_UPDATE_FEILD')

class TestUserInformation(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User(firstName="test", lastName="test", email="test@gmail.com", username="test", folderName="test", password="test")
        self.user.save()
    
    def tearDown(self):
        # Brisanje testnog foldera nakon testa
        if os.path.exists("media"):
            shutil.rmtree("media")

    def test_getUserInformationWithUserIdIsCorectly_success(self):
        response = self.c.get('/user-information/' + str(self.user.id), HTTP_AUTHORIZATION='', content_type=JSON)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'followers')
        self.assertContains(response, 'following')


    def test_getUserInformationWithUserIdIsNotCorectly_feild(self):
        response = self.c.get('/user-information/1999', HTTP_AUTHORIZATION='', content_type=JSON)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'USER_NOT_FOUND')