from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import os

class CustomUser(AbstractUser):
    family_members = models.ManyToManyField("self", symmetrical=False, blank=True, verbose_name="Familienmitglieder")
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
        verbose_name="Profilbild"
    )

    def save(self, *args, **kwargs):
        is_new_user = self.pk is None

        # Temporär Bild sichern
        original_picture = self.profile_picture

        if not is_new_user:
            try:
                old_user = CustomUser.objects.get(pk=self.pk)
                if old_user.profile_picture and old_user.profile_picture != self.profile_picture:
                    default_storage.delete(old_user.profile_picture.name)
            except CustomUser.DoesNotExist:
                pass

        # Erstmal ohne Bild speichern, um PK zu bekommen
        if is_new_user:
            temp_picture = self.profile_picture
            self.profile_picture = None
            super().save(*args, **kwargs)
            self.profile_picture = temp_picture

        # Bild verarbeiten, falls vorhanden
        if original_picture:
            try:
                image = Image.open(original_picture)
                if image.mode != 'RGB':
                    image = image.convert('RGB')

                buffer = BytesIO()
                image.save(buffer, format='PNG')
                filename = f"profile_pictures/{self.pk}_img.png"
                self.profile_picture.save(filename, ContentFile(buffer.getvalue()), save=False)
            except Exception as e:
                print(f"[Fehler beim Bildverarbeiten] {e}")
                self.profile_picture = None

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.profile_picture:
            default_storage.delete(self.profile_picture.name)
        super().delete(*args, **kwargs)


class Family(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Familienname")
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="admin_of_families", verbose_name="Admin")
    members = models.ManyToManyField(CustomUser, related_name="families", blank=True, verbose_name="Mitglieder")
    created_at= models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")

    def __str__(self):
        return self.name


class UserSettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="settings")
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
    icons = models.CharField(  # Add this field
        max_length=50,
        default="default",  # Provide an appropriate default
        verbose_name="Icons"
    )

    def __str__(self):
        return f"Einstellungen für {self.user.username}"