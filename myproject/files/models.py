from django.db import models
from users.models import User
from datetime import datetime


def upload_path(instance, filname):
    splits = filname.split("_")
    link = ""
    index = len(splits)
    count = 0
    for each in splits:
        link += each
        count = count + 1
        if count < index:
            link += "/"
    return "/".join(["covers", link])

# Create your models here.


class Files(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    cover = models.FileField(blank=True, null=True, upload_to=upload_path)
    dateCreate = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def find_by_id(self, id):
        try:
            return Files.objects.get(id=id)
        except Files.DoesNotExist:
            return None

    def create(self, name, content, user):
        return Files.objects.create(
            name=name,
            cover=content,
            dateCreate=datetime.now(),
            user=user
        )