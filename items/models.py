from django.db import models
from users.models import User


class BuyHistory(models.Model):
    name = models.TextField()
    amount = models.IntegerField()
    price = models.IntegerField()
    total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.TextField()

    class Meta:
        ordering = ['-created_at']
