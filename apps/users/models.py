from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    user_document = models.CharField(max_length=50)
    user_address = models.CharField(max_length=100)
    user_email = models.EmailField()
    user_phone_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.user_name} ({self.user_document})"
