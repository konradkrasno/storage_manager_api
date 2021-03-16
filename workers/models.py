from django.db import models


class Worker(models.Model):
    """
    Identifies company employees.
    """

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    position = models.CharField(max_length=20)
    active = models.BooleanField()

    def __str__(self):
        return f"<Worker: {self.first_name} {self.last_name}>"
