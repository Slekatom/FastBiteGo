from django.db import models
from menu.models import Meal
from accounts.models import CustomUser

user = CustomUser
class Order(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(user, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.meal}"

class Cart(models.Model):

    STATUS = [
        ("In progress", "In progress"),
        ("History", "History"),
    ]


    date_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS, default = "In progress")
    user = models.ForeignKey(user, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.date_time} was created a new cart ({self.status})"

class CartItems(models.Model):
    meal = models.ForeignKey(Meal, on_delete = models.CASCADE)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.meal} ---> {self.cart}"
