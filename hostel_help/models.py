from django.db import models


# Create your models here.
class Report(models.Model):
    PROBLEM_CHOICES = (("Електрик", "Електрик"),
                       ("Столяр", "Столяр"),
                       ("Сантехнік", "Сантехнік"),
                       ("Не визначено", "Не визначено"))
    DORMITORIES_CHOICES = ((3, "3 гуртожиток"),
                           (4, "4 гуртожиток"),
                           (5, "5 гуртожиток"),
                           (7, "7 гуртожиток"),
                           (8, "8 гуртожиток"),
                           (12, "12 гуртожиток"),
                           (13, "13 гуртожиток"),
                           (14, "14 гуртожиток"),
                           (15, "15 гуртожиток"),
                           (16, "16 гуртожиток"),
                           (17, "17 гуртожиток"),
                           (18, "18 гуртожиток"),
                           (19, "19 гуртожиток"),
                           (20, "20 гуртожиток"),
                           (21, "21 гуртожиток"),
                           (22, "22 гуртожиток"),)

    email = models.EmailField(max_length=80, default=False)
    title = models.CharField(max_length=70)
    problem_type = models.CharField(choices=PROBLEM_CHOICES, max_length=70, default="Не визначено")
    dormitory = models.IntegerField(choices=DORMITORIES_CHOICES)
    exact_place = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Неактивна")

    def __str__(self):
        return f"{self.title} {self.date}"


class Contact(models.Model):
    report_id = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="contact_emails")
    date_report = models.DateTimeField()
    date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=80)
    message = models.TextField()
