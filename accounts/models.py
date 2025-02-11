from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    family_members = models.ManyToManyField("self", symmetrical=False,blank = True, verbose_name="Familienmitglieder")

    pass
class UserSettings(models.Model):
    user =models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="settings")
    design = models.CharField(max_length=10, choices=[
        ("black", "Schwarz"),
        ("white", "Weiß"),
        ("colored", "Colored")
          ],
        default="colored", verbose_name="Design")
    icons = models.CharField(max_length=10, choices=[
        ("black", "Schwarz"),
        ("white", "Weiß"),
        ("colored", "Colored")
          ],
        default="colored", verbose_name="Icons")
    
    def __str__(self):
        return f"Einstellungen für {self.user.username}"