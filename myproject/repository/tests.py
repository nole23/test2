import os
import shutil
from django.test import Client, TestCase
from repository.service import RepositoryService
from users.models import User
import json

JSON = 'application/json'

# Create your tests here.
class TestRepositoryLogin(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User(firstName="test", lastName="test", email="test@gmail.com", username="test", folderName="test", password="test")
        self.user.save()

        self.user1 = User(firstName="test1", lastName="test1", email="test1@gmail.com", username="test1", folderName="test1", password="test1")
        self.user1.save()

        user = {
            'id': self.user.id, 
            'firstName': self.user.firstName, 
            'lastName': self.user.lastName, 
            'username': self.user.username, 
        }

        repository = RepositoryService()
        repositoryData = {
            'projectName': 'test2', 
            'type': 'Private', 
            'descriotion': '', 
            'typeLanguage': 'Python', 
            'typeLicense': 'PRIVATE', 
            'dateOfModifide': '2024-08-15T16:00:59.385Z',
            'user': user
        }
        self.repositorySave = repository.createRepository(repositoryData)

    def tearDown(self):
        # Brisanje testnog foldera nakon testa
        if os.path.exists("media"):
            shutil.rmtree("media")
    
    def test_getAllRepositoryByUserId_retrunAllRepositorySuccess(self):
        response = self.c.get('/all-repository/' + str(self.user.id), HTTP_AUTHORIZATION='', content_type=JSON)
        
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data), 1)
    
    def test_getAllRepositoryByIncorenctUserId_retrunEmptyList(self):
        response = self.c.get('/all-repository/' + str(self.user1.id), HTTP_AUTHORIZATION='', content_type=JSON)
        
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data), 0)
    
    def test_getAllRepositoryByIncorenctUserId_retrunFalse(self):
        response = self.c.get('/all-repository/1999', HTTP_AUTHORIZATION='', content_type=JSON)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'USER_NOT_FOUND')
    
    def test_createNewRepository_true(self):
        repositoryData1 = {
            'projectName': 'test3', 
            'type': 'Private', 
            'descriotion': '', 
            'typeLanguage': 'Python', 
            'typeLicense': 'PRIVATE', 
            'dateOfModifide': '2024-08-15T16:00:59.385Z',
            'user': {
                'id': self.user.id, 
                'firstName': self.user.firstName, 
                'lastName': self.user.lastName, 
                'username': self.user.username, 
            }
        }
        response = self.c.post('/new-repository', json.dumps(repositoryData1), HTTP_AUTHORIZATION='', content_type=JSON)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'typeLanguage')

    def test_createNewRepositoryWithIncorenctUser_false(self):
        repositoryData1 = {
            'projectName': 'test3', 
            'type': 'Private', 
            'descriotion': '', 
            'typeLanguage': 'Python', 
            'typeLicense': 'PRIVATE', 
            'dateOfModifide': '2024-08-15T16:00:59.385Z',
            'user': {
                'id': '1999', 
                'firstName': self.user.firstName, 
                'lastName': self.user.lastName, 
                'username': self.user.username, 
            }
        }
        response = self.c.post('/new-repository', json.dumps(repositoryData1), HTTP_AUTHORIZATION='', content_type=JSON)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'USER_NOT_FOUND')
    
    def test_updatereRepository_successifull(self):
        repositoryData1 = {
            'id': self.repositorySave['id'],
            'name': 'NewName', 
            'type': self.repositorySave['type'], 
            'descriotion': self.repositorySave['descriotion'], 
            'typeLanguage': self.repositorySave['typeLanguage'], 
            'typeLicense': self.repositorySave['typeLicense'], 
            'dateOfModifide': self.repositorySave['dateOfModifide']
        }
        response = self.c.put('/update-repository/general', json.dumps(repositoryData1), HTTP_AUTHORIZATION='', content_type=JSON)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'NewName')
    
    def test_updatereRepositoryIncorectId_false(self):
        repositoryData1 = {
            'id': 1999,
            'name': 'NewName', 
            'type': self.repositorySave['type'], 
            'descriotion': self.repositorySave['descriotion'], 
            'typeLanguage': self.repositorySave['typeLanguage'], 
            'typeLicense': self.repositorySave['typeLicense'], 
            'dateOfModifide': self.repositorySave['dateOfModifide']
        }
        response = self.c.put('/update-repository/general', json.dumps(repositoryData1), HTTP_AUTHORIZATION='', content_type=JSON)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PROJECT_NOT_FOUND')

class TestRepositoryUser(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User(firstName="test", lastName="test", email="test@gmail.com", username="test", folderName="test", password="test")
        self.user.save()

        self.user1 = User(firstName="test1", lastName="test1", email="test1@gmail.com", username="test1", folderName="test1", password="test1")
        self.user1.save()

        user = {
            'id': self.user.id, 
            'firstName': self.user.firstName, 
            'lastName': self.user.lastName, 
            'username': self.user.username, 
        }

        repository = RepositoryService()
        repositoryData = {
            'projectName': 'test2', 
            'type': 'Private', 
            'descriotion': '', 
            'typeLanguage': 'Python', 
            'typeLicense': 'PRIVATE', 
            'dateOfModifide': '2024-08-15T16:00:59.385Z',
            'user': user
        }
        self.repositorySave = repository.createRepository(repositoryData)
    
    def tearDown(self):
        # Brisanje testnog foldera nakon testa
        if os.path.exists("media"):
            shutil.rmtree("media")
    
    def test_addUserToProject_true(self):
        response = self.c.get('/add-user-repository/' + str(self.user1.id) + '/' + str(self.repositorySave['id']), HTTP_AUTHORIZATION='', content_type=JSON)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SAVE_IS_SUCCESS')
    
    def test_addUserToProject_true(self):
        response = self.c.get('/add-user-repository/1999/' + str(self.repositorySave['id']), HTTP_AUTHORIZATION='', content_type=JSON)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'USER_NOT_FOUND')

    def test_addUserToProject_true(self):
        response = self.c.get('/add-user-repository/' + str(self.user1.id) + '/1999', HTTP_AUTHORIZATION='', content_type=JSON)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PROJECT_NOT_FOUND')