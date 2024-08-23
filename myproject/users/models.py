from django.db import models
import random

class Role(models.Model):
    ROLES = (
        ('O', 'Owner'),
        ('C', 'Collaborator'),
        ('V', 'Visitor'),
    )
    id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=1, choices=ROLES)

    def get_by_id(self, id):
        try:
            return Role.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def get_by_role_name(self, name):
        try:
            role = Role.objects.get(role_name=name)
            return role
        except Role.DoesNotExist:
            return None

class UserInformation(models.Model):
    id = models.AutoField(primary_key=True)
    imageLink = models.CharField(max_length=30)

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    folderName = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    userInformation = models.ForeignKey(UserInformation, on_delete=models.CASCADE, null=True)

    def get_by_username(self, username):
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            return None

    def get_all_by_email(self, email):
        try:
            return User.objects.filter(email__exact=email)
        except User.DoesNotExist:
            return None

    def get_all(self):
        return User.objects.all()

    def get_by_id(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def create_new_user(self, data):
        username = data['email'].split('@')
        username = username[0]
        random_number = random.randint(1, 5)

        ui = UserInformation.objects.create(
            imageLink = str(random_number) + ".png"
        )

        User.objects.create(
            firstName=data['firstName'],
            lastName=data['lastName'],
            email=data['email'],
            username=username,
            folderName=username,
            password=data['password'],
            userInformation=ui
        )

    def update(self, data):
        try:
            data.save()
        except User.DoesNotExist:
            return None

    def filter(self, text):
        try:
            return User.objects.filter(firstNamestartswith=text) | User.objects.filter(lastNamestartswith=text) | User.objects.filter(email__startswith=text)
        except User.DoesNotExist:
            return None

    def filterByText(self, text):
        try:
            return User.objects.filter(username__startswith=text, firstName__startswith=text, lastName__startswith=text, email__startswith=text)
        except User.DoesNotExist:
            return None