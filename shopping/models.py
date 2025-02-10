from django.db import models
from django.contrib.auth import get_user_model

class ShoppingItem(models.Model):
    name = models.CharField(max_length=100, verbose_name="Artikel")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Menge")
    added_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Hinzugefügt von")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Hinzugefügt am")
    completed = models.BooleanField(default=False, verbose_name="Erledigt")

    def __str__(self):
        return f"{self.name} ({self.quantity})"