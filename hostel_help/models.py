from django.db import models

class Report(models.Model):
    title = models.CharField(max_length=70)
    problem_type =  models.CharField(max_length=70)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} {self.date}"
