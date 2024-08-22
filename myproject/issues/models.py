from django.db import models
from datetime import datetime
from users.models import User
from repository.models import Project

# Create your models here.

class Issue(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=150)
    status = models.BooleanField(default=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    dateCreate = models.DateTimeField(null=True, blank=True)
    assigned = models.ManyToManyField(
        User, blank=True, related_name='assigned')
    labels = models.CharField(max_length=99999, null=True)

    def get_by_id(self, id):
        try:
            return Issue.objects.get(id=id)
        except Issue.DoesNotExist:
            return None

    def filter_issue_by_user_status(self, project, trueOrFalse, user):
        try:
            return Issue.objects.filter(project=project, status=trueOrFalse, user=user)
        except Issue.DoesNotExist:
            return None

    def filter_issue_by_user(self, project, user):
        try:
            return Issue.objects.filter(project=project, user=user)
        except Issue.DoesNotExist:
            return None

    def filter_issue_by_status(self, project, trueOrFalse):
        try:
            return Issue.objects.filter(project=project, status=trueOrFalse)
        except Issue.DoesNotExist:
            return None

    def filter_issue(self, project):
        try:
            return Issue.objects.filter(project=project)
        except Issue.DoesNotExist:
            return None
    
    def filter_data_issue(self, data):
        return Issue.objects.filter(dateCreate__month=data)

    def create(self, data, project, user):
        issue = Issue.objects.create(
            name=data['name'],
            description=data['description'],
            project=project,
            user=user,
            dateCreate=datetime.now(),
            labels=data['labels']
        )
        return issue

class IssueComment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=150)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreate = models.DateTimeField(null=True, blank=True)
    typeComment = models.CharField(max_length=150, default='COMMENT')

    def create(self, comment, issue, user, typeComment):
        try:
            return IssueComment.objects.create(
                comment=comment,
                issue=issue,
                user=user,
                dateCreate=datetime.now(),
                typeComment=typeComment
            )
        except Exception:
            return None

    def filterByIssue(self, issue):
        try:
            return IssueComment.objects.filter(issue=issue)
        except Exception:
            return None