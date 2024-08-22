from django.db import models
from datetime import datetime

from users.models import User, Role
from files.models import Files

# Create your models here.


class ChildrenTree(models.Model):
    id = models.AutoField(primary_key=True)
    name_node = models.CharField(max_length=150)
    date_create = models.DateTimeField(null=True, blank=True)
    user_create = models.ForeignKey(User, on_delete=models.CASCADE)
    files = models.ManyToManyField(Files, blank=True)
    childrenFolder = models.ManyToManyField(
        'self', blank=True, symmetrical=False, related_name='childrenTree')


class RootTree(models.Model):
    id = models.AutoField(primary_key=True)
    nameBranch = models.CharField(max_length=150)
    dateCreate = models.DateTimeField(null=True, blank=True)
    userCreate = models.ForeignKey(User, on_delete=models.CASCADE)
    files = models.ManyToManyField(Files, blank=True)
    childrenFolder = models.ManyToManyField(ChildrenTree, blank=True)

    def createRoot(self, branch, user, files):
        rootTree = RootTree.objects.create(
            nameBranch=branch,
            dateCreate=datetime.now(),
            userCreate=user
        )
        rootTree.files.add(files)
        return rootTree


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=150)
    dateCreate = models.DateTimeField(null=True, blank=True)
    dateClose = models.DateTimeField(null=True, blank=True)
    typeProject = models.BooleanField(null=True, blank=True)
    typeLicense = models.CharField(max_length=30)
    typeLanguage = models.CharField(max_length=30)
    rootTree = models.ManyToManyField(RootTree, blank=True)

    def create(self, name, description, typeProject, rootTree, typeLicense, typeLanguage):
        project = Project.objects.create(
            name=name,
            description=description,
            dateCreate=datetime.now(),
            typeProject=typeProject,
            typeLanguage=typeLanguage,
            typeLicense=typeLicense
        )
        project.rootTree.add(rootTree)
        return project

    def get_by_id(self, id):
        try:
            return Project.objects.get(id=id)
        except Project.DoesNotExist:
            return None

    def delete(self, id):
        project = Project.objects.get(id=id)
        project.delete()
        return project


class ListProjectUser(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)

    def filter_by_id(self, id):
        try:
            return ListProjectUser.objects.filter(project_id=id)
        except ListProjectUser.DoesNotExist:
            return None

    def filter_by_user(self, user):
        try:
            return ListProjectUser.objects.filter(user=user)
        except ListProjectUser.DoesNotExist:
            return None

    def filter_by_user_type(self, user, type):
        return ListProjectUser.objects.filter(user=user, project__typeProject=type)

    def filter_by_name_project(self, user, text):
        return ListProjectUser.objects.filter(user=user, project__name__contains=text)

    def create(self, project, user, role):
        ListProjectUser.objects.create(
            project=project,
            user=user,
            role=role
        ) 