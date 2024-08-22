from django.db import models
from repository.models import Project
from files.models import Files

# Create your models here.

class Statistic(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    files = models.ForeignKey(Files, on_delete=models.CASCADE)
    dateCreate = models.DateTimeField(null=True, blank=True)

    def findByProjct(self, project):
        try:
            project = Statistic.objects.filter(project=project)
            return project
        except Statistic.DoesNotExist:
            return None