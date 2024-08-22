# import os
# import shutil
# from django.test import Client, TestCase

# from repository.service import RepositoryService
# from users.models import User

# JSON = 'application/json'

# # Create your tests here.
# class TestLogin(TestCase):
#     def setUp(self):
#         self.c = Client()
#         userSave = User.objects.create(firstName="test", lastName="test", email="test@gmail.com", username="test", folderName="test", password="test")
#         user = {
#             'id': userSave.id, 
#             'firstName': userSave.firstName, 
#             'lastName': userSave.lastName, 
#             'username': userSave.username, 
#         }

#         repository = RepositoryService()
#         repositoryData = {
#             'projectName': 'test2', 
#             'type': 'Private', 
#             'descriotion': '', 
#             'typeLanguage': 'Python', 
#             'typeLicense': 'PRIVATE', 
#             'dateOfModifide': '2024-08-15T16:00:59.385Z',
#             'user': user
#         }
#         self.repositorySave = repository.createRepository(repositoryData)
    
#     def tearDown(self):
#         # Brisanje testnog foldera nakon testa
#         if os.path.exists("media"):
#             shutil.rmtree("media")

#     def test_getStatisticByRepositoryId_successifull(self):
#         response = self.c.get('/statistic/' + self.repositorySave['id'], HTTP_AUTHORIZATION='', content_type=JSON)

#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'count_of_ammount')
    
#     def test_getStatisticByIncorectyRepositoryId_successifull(self):
#         response = self.c.get('/statistic/1999', HTTP_AUTHORIZATION='', content_type=JSON)

#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'PROJECT_NOT_FOUND')