from django.db import models


class User(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    password = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "user"
        verbose_name = "App user"

    def __str__(self) -> str:
        return f"User {self.name}"
