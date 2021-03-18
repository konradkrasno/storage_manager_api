from django.db import models
from accounts.models import User


class Worker(models.Model):
    """
    Identifies company employees.
    """

    position = models.CharField(max_length=20)
    user = models.OneToOneField(User, related_name="worker", on_delete=models.CASCADE)

    def __str__(self):
        return f"<Worker: {self.user.first_name} {self.user.last_name}>"
