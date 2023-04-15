from django.db import models


class Session(models.Model):
    user = models.ForeignKey(
        "user.User", models.DO_NOTHING, db_column="user", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "session"
        verbose_name = "User session"

    def __str__(self) -> str:
        return f"User session {self.user_id}: {self.user.name}"
