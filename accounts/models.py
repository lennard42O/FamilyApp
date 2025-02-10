from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    family_members = models.ManyToManyField("self", symmetrical=False,blank = True, verbose_name="Familienmitglieder")

    pass