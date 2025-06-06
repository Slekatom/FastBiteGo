from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Category(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=50)
    media = models.ImageField(upload_to='media/category')

    def __str__(self):
        return f"Category {self.title}"

class Meal(models.Model):
    TYPE = {("New", "New"),
            ("Trending", "Trending"),
            ("Default", "Default")}

    title = models.CharField(max_length=30)
    description = models.TextField(max_length=50)
    media = models.ImageField(upload_to='media/category')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank = True, null = True)
    type = models.CharField(max_length=30, choices=TYPE, default="Default")
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} in category {self.category}"

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.TextField(max_length=30)
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"{self.user} reviewed on {self.meal}: {self.title} -> {self.rating}"