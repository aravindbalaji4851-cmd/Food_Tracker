from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Foodlog(models.Model):

    MEAL_TYPES = (
        ("Breakfast","Breakfast"),
        ("Lunch","Lunch"),
        ("Dinner","Dinner"),
        ("Snacks","Snacks")
        )

    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    calorie = models.PositiveIntegerField()

    meal_type = models.CharField(max_length=20,choices=MEAL_TYPES)

    serving_size = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    