from django.db import models


class User(models.Model):
    class Meta:
        db_table = "user"
        verbose_name = "Кастомный пользователь"

    name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"Пользователь {self.name}"
