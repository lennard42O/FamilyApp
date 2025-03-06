from django import models
from django.contrib.auth import get_user_model

class MealPlan(model.Model):
    user = models.ForeignKey(get_user_model),on_delete=models.CASCADE, related_name="meals_plans"