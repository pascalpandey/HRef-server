from django.db import models

class Candidate(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    keywords = models.JSONField(default=list)  # Store keywords as a JSON array
    color = models.CharField(max_length=255)
    resume_link = models.URLField()
    score = models.DecimalField(max_digits=3, decimal_places=1)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return self.id

class Employee(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    keywords = models.JSONField(default=list)
    color = models.CharField(max_length=255)
    resume_link = models.URLField()
    score = models.DecimalField(max_digits=3, decimal_places=1)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return self.id
