from django.db import models
from cart.models import *
from accounts.models import CustomUser

user_c = CustomUser

class Payment(models.Model):
    CHOICES = [("Cash", "Cash"), ("Card", "Card")]
    CONFIRMED_STATUS = [
        ("Not Confirmed", "Not Confirmed"),
        ("Confirmed", "Confirmed")
    ]
    PURCHASE = [
        ("Purchased", "Purchased"),
        ("Not Purchased", "Not Purchased"),
    ]
    ARRIVE_STATUS = [
        ("Arrived", "Arrived"),
        ("Not Arrived", "Not Arrived")
    ]

    user = models.ForeignKey(user_c, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    choices = models.CharField(max_length=30, choices=CHOICES)
    confirmed_status = models.CharField(max_length=30, choices=CONFIRMED_STATUS, default="Not Confirmed")
    purchase = models.CharField(max_length=30, choices=PURCHASE, default="Not Purchased")
    arrive_status = models.CharField(max_length=30, choices=ARRIVE_STATUS, default="Not Arrived")

    def __str__(self):
        return f"{self.cart} is {self.purchase}"