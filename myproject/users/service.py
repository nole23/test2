from users.models import User
from datetime import datetime, timedelta
import jwt
from common.webCommon import AuthSerialize
from common.webCommon import ResponsObject 

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 84600

class UserService(AuthSerialize):
    userModel = User()
    responseObject = ResponsObject()

    def login(self, data):
        user = self.userModel.get_by_username(data['username'])
        if user is None:
            return {"status": "FALSE", "data": "USER_NOT_FOUND"}

        if user.password != data['password']:
            return {"status": "FALSE", "data": "PASSWORD_NOT_FOUND"}

        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
        }

        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

        return {"status": "SUCCESS", "data": self.loginSerialize(user, jwt_token)}

    def getUserById(self, id):
        user = self.userModel.get_by_id(id)
        if user is None:
            return {"status": "FALSE", "message": "USER_NOT_FOUND"}
        return user
    
    def filter(self, text):
        users = self.userModel.filterByText(text)
        if users is None:
            return {"status": "FALSE", "message": "USER_NOT_FOUND"} 
        return self.responseObject.usersSerialize(users)

    def registration(self, data):
        users = self.userModel.get_all_by_email(data['email'])

        if users is None:
            return {"status": "FALSE", "message": "USER_NOT_FOUND"}

        if users.count() > 0:
            return {"status": "FALSE", "data": "NOT_SAVE_MAIL"}

        self.userModel.create_new_user(data)
        return {"status": "SUCCESS", "data": None}
    
    def update(self, data):
        user = self.userModel.get_by_id(data['id'])
        if user is None:
            return {"status": "FALSE", "message": "USER_NOT_FOUND"}

        isUpdate = False

        if 'firstName' in data:
            user.firstName = data['firstName']
            isUpdate = True

        if 'lastName' in data:
            user.lastName = data['lastName']
            isUpdate = True
        
        if 'username' in data:
            user.username = data['username']
            isUpdate = True
        
        if isUpdate:
            user.save()
            return {"status": "SUCCESS", "user": self.responseObject.userSerialize(user)}
        else:
            return {"status": "FALSE", "message": "NOT_UPDATE_FEILD"}
    
    def getAllInformation(self, id):
        user = self.userModel.get_by_id(id)
        if user is None:
            # ovde treba da se napravi ostala logika za cupanje informacija
            return {"status": "FALSE", "message": "USER_NOT_FOUND"}
        
        return {"status": "SUCCESS", "data": {"followers": 0, "following": 0}}

    def getAllUser(self):
        test = self.userModel.get_all()
        return self.responseObject.usersSerialize(test)
