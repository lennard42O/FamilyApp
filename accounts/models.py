from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import uuid


class CustomUser(AbstractUser):
    family_members = models.ManyToManyField("self", symmetrical=False, blank=True, verbose_name="Familienmitglieder")
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
        verbose_name="Profilbild"
    )

    def save(self, *args, **kwargs):
        old_profile_picture = None
        if self.pk:
            try:
                old_user = CustomUser.objects.get(pk=self.pk)
                old_profile_picture = old_user.profile_picture
            except CustomUser.DoesNotExist:
                pass

        if not self.pk:
            super().save(*args, **kwargs)

        if old_profile_picture and old_profile_picture != self.profile_picture:
            try:
                default_storage.delete(old_profile_picture.name)
            except FileNotFoundError:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Old profile picture not found for user {self.username}")

        if self.profile_picture:
            try:
                filename = f"{self.pk}_img.png"

                if not self.profile_picture.name.endswith('.png'):
                    image = Image.open(self.profile_picture)
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    buffer = BytesIO()
                    image.save(buffer, format='PNG')
                    self.profile_picture.save(filename, ContentFile(buffer.getvalue()), save=False)
                else:
                    self.profile_picture.name = filename

                self.profile_picture.save(self.profile_picture.name, self.profile_picture.file, save=False)
            except FileNotFoundError:
                self.profile_picture = None
            
        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        if self.profile_picture:
            default_storage.delete(self.profile_picture.name)
        super().delete(*args, **kwargs)


class UserSettings(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="settings")
    design = models.CharField(
        max_length=10,
        choices=[
            ("black", "Schwarz"),
            ("white", "Weiß"),
            ("colored", "Colored")
        ],
        default="colored",
        verbose_name="Design"
    )

    def __str__(self):
        return f"Einstellungen für {self.user.username}"
