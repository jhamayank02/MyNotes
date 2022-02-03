from django.db import models
from django.utils.timezone import now

# Create your models here.
class Note(models.Model):
    sno = models.AutoField(primary_key=True)
    author = models.CharField(max_length=20)
    timeStamp = models.DateTimeField(default=now)
    noteHeading = models.TextField()
    noteContent = models.TextField()
    tag = models.CharField(max_length=50, blank=True, null=True)
    deadlineDate = models.DateField(blank=True, null=True)
    deadlineTime = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.noteHeading
    
