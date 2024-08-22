import os
import shutil
from django.test import Client, TestCase
from issues.service import IssueService
from repository.service import RepositoryService
from users.models import User
import json

JSON = 'application/json'

# Create your tests here.
class TestIssue(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User(firstName="test", lastName="test", email="test@gmail.com", username="test", folderName="test", password="test")
        self.user.save()

        self.userJSON = {
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
            'user': self.userJSON
        }
        self.repositorySave = repository.createRepository(repositoryData)

    def tearDown(self):
        # Brisanje testnog foldera nakon testa
        if os.path.exists("media"):
            shutil.rmtree("media")

    def test_addNewIssues_successifull(self):
        newIssues = {
            "name": "testName",
            "description": "testDescription",
            "id": self.repositorySave['id'],
            "labels": "null",
            "user": self.userJSON,
            "project": "null"

        }
        response = self.c.post('/add-issue', json.dumps(newIssues), HTTP_AUTHORIZATION='', content_type=JSON)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testDescription')
    
    def test_addNewIssuesForNotExistProject_false(self):
        newIssues = {
            "name": "testName",
            "description": "testDescription",
            "id": "1999",
            "labels": "null",
            "user": self.userJSON,
            "project": "null"

        }
        response = self.c.post('/add-issue', json.dumps(newIssues), HTTP_AUTHORIZATION='', content_type=JSON)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PROJECT_NOT_FOUND')
    
    def test_addNewIssuesForNotExistUser_false(self):
        userJSON = {
            'id': "1999", 
            'firstName': self.user.firstName, 
            'lastName': self.user.lastName, 
            'username': self.user.username, 
        }
        newIssues = {
            "name": "testName",
            "description": "testDescription",
            "id": self.repositorySave['id'],
            "labels": "null",
            "user": userJSON,
            "project": "null"

        }
        response = self.c.post('/add-issue', json.dumps(newIssues), HTTP_AUTHORIZATION='', content_type=JSON)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'USER_NOT_FOUND')   

    def test_closeIssue_successifull(self):
        newIssues = {
            "name": "testName",
            "description": "testDescription",
            "id": self.repositorySave['id'],
            "labels": "null",
            "user": self.userJSON,
            "project": "null"

        }
        response = self.c.post('/add-issue', json.dumps(newIssues), HTTP_AUTHORIZATION='', content_type=JSON)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testDescription')

        reposnse_data = json.loads(response.content)

        closeIssue = {
            "data": {
                "id": reposnse_data['id']
            },
            "user": self.userJSON
        }

        res = self.c.put('/close-issue', json.dumps(closeIssue), HTTP_AUTHORIZATION='', content_type=JSON)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, '"status": false')

class TestIssuesGet(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User(firstName="test", lastName="test", email="test@gmail.com", username="test", folderName="test", password="test")
        self.user.save()

        self.userJSON = {
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
            'user': self.userJSON
        }
        self.repositorySave = repository.createRepository(repositoryData)

        newIssues = {
            "name": "testName",
            "description": "testDescription",
            "id": self.repositorySave['id'],
            "labels": "null",
            "user": self.userJSON,
            "project": "null"

        }

        issue = IssueService()
        self.issueSave = issue.createNewIssue(self.userJSON, newIssues)

        newIssueComment = {
            "id": self.issueSave['id'],
            "comment": "testComment"
        }
        self.issueCommentSave = issue.createNewComment(self.userJSON, newIssueComment)

    def tearDown(self):
        # Brisanje testnog foldera nakon testa
        if os.path.exists("media"):
            shutil.rmtree("media")
    
    def test_getIssueById_returnIssue(self):
        response = self.c.get('/issue/' + str(self.issueSave['id']), HTTP_AUTHORIZATION='', content_type=JSON)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testDescription')

    def test_getIssueByIncorectId_returnFalse(self):
        response = self.c.get('/issue/1999', HTTP_AUTHORIZATION='', content_type=JSON)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ISSUE_NOT_FOUNE')

    def test_assignedUserToIssue_true(self):
        assignedToIssue = {
            "user": self.userJSON,
            "data": {
                "id": self.issueSave['id']
            }
        }
        response = self.c.put('/assigne-issue', json.dumps(assignedToIssue), HTTP_AUTHORIZATION='', content_type=JSON)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test test assigned to issue #1.')