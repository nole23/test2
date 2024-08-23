from rest_framework.views import APIView
from common.webCommon import ResponsObject
from users.models import User, Role, UserInformation
from users.service import UserService
from common.webCommon import decode_body
import random

"""
Ovde se nalazi logika za get post put i delete indexne stranice.
Na ovaj nacin cemo uraditi kompletnu aplikaciju. Dodavacemo novu
klasu ukoliko nam je potrebno nesto specificno
"""
class Index(APIView):
    def __init__(self):
        self.res = ResponsObject()
    
    def get(self, request):

        random_number = random.randint(1, 5)

        image = str(random_number) + ".png"
        # defaultni user kog kreiramo
        ui = UserInformation(imageLink=image)
        ui.save()

        user = User(firstName="test", lastName="test", email="test@gmail.com", username="test", folderName="test", password="test", userInformation=ui)
        user.save()

        role1 = Role(role_name="O")
        role2 = Role(role_name="C")
        role3 = Role(role_name="V")

        role1.save()
        role2.save()
        role3.save()
        self.res.addItem({"message": "SUCCESS", "data": "Test server resoponse."})
        
        return self.res.createResponse(status=200)

class Login(APIView):
    user = UserService()

    def __init__(self):
        self.res = ResponsObject()

    def post(self, request):
        data = decode_body(request.body)
        login = self.user.login(data)

        self.res.addItem(login)

        return self.res.createResponse(status=200)

class Registration(APIView):
    user = UserService()

    def __init__(self):
        self.res = ResponsObject()

    def post(self, request):
        data = decode_body(request.body)
        registration = self.user.registration(data)

        self.res.addItem(registration)

        return self.res.createResponse(status=200)
    
class User1(APIView):
    user = UserService()

    def __init__(self):
        self.res = ResponsObject()

    def get(self, _, text):
        users = self.user.filter(text)
        self.res.addItem(users)
        return self.res.createResponse(status=200)
    
    def put(self, request):
        data = decode_body(request.body)
        updateUsers = self.user.update(data)
        self.res.addItem(updateUsers)
        return self.res.createResponse(status=200)
    
class UserInformation1(APIView):
    user = UserService()

    def __init__(self):
        self.res = ResponsObject()
    
    def get(self, _, id):
        userInformation = self.user.getAllInformation(id)
        self.res.addItem(userInformation)
        return self.res.createResponse(status=200)
    


class UserTest(APIView):
    user = UserService()

    def __init__(self):
        self.res = ResponsObject()

    def get(self, _):
        user = self.user.getAllUser()
        self.res.addItem(user)
        return self.res.createResponse(status=200)