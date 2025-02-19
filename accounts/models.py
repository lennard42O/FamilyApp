# accounts/models.py
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
    family_members = models.ManyToManyField("self", symmetrical=False,blank = True, verbose_name="Familienmitglieder")
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
        verbose_name="Profilbild"
    )

    def save(self, *args, **kwargs):
        # Get the old profile picture name before saving
        try:
            old_user = CustomUser.objects.get(pk=self.pk)
            old_picture_name = old_user.profile_picture.name if old_user.profile_picture else None
        except CustomUser.DoesNotExist:
            old_picture_name = None

        super().save(*args, **kwargs)  # Save the user first to get the pk

        if self.profile_picture:
            # Generate the new filename
            filename = f"{self.pk}_img.png"
            new_path = os.path.join("profile_pictures", filename)

            # Get the current extension
            ext = self.profile_picture.name.split('.')[-1]
            # If the extension is not png, convert it
            if ext != 'png':
                # Convert the image to PNG
                from PIL import Image
                from io import BytesIO

                # Open the image
                image = Image.open(self.profile_picture)
                # Convert to RGB if necessary
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                # Save as PNG
                buffer = BytesIO()
                image.save(buffer, 'png')
                # Create a new ContentFile with the PNG data
                from django.core.files.base import ContentFile
                self.profile_picture.file = ContentFile(buffer.getvalue(), filename)
                self.profile_picture.name = filename
            else:
                # Rename the file
                self.profile_picture.name = filename

            # Save the file with the new name
            self.profile_picture.save(new_path, self.profile_picture.file, save=False)

        # Delete the old profile picture
        if old_picture_name and self.profile_picture.name != old_picture_name:
            default_storage.delete(old_picture_name)

        super().save(*args, **kwargs)

    def delete(self, *args,**kwargs):
        if self.profile_picture:
            default_storage.delete(self.profile_picture.name)
        super().delete(*args,**kwargs)

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
