from django.db import models
from django.contrib.auth.models import User

priorities = (("1", "HIGH"),
            ("2", "MODERATE"),
            ("3", "LOW"))

order_by = (("date_created", "Date up"),
            ("-date_created", "Date downscending"),
            ("priority", "Priority ascending "),
            ("-priority", " Priority downscending"),
            ("to_be_done_date", "Done date ascending"),
            ("-to_be_done_date", "Done date downscending"),
            ("is_done", "Finished"),
            ("-is_done", "Not finished"))


# Create your models here.
class List(models.Model):
    name = models.CharField(max_length=124, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    ordered_by = models.CharField(max_length=120, choices=order_by, default="date_created")
    user = models.ForeignKey(User, related_name="lists", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=124, blank=False)
    date_created = models.DateField(auto_now_add=True)
    to_be_done_date = models.DateField(null=True)
    list = models.ForeignKey(List, related_name="tasks", on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=priorities)


    def __str__(self):
        return self.name

