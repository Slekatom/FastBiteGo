from django.db import models
from accounts.models import CustomUser
from cart.models import Cart
User = CustomUser

class Request(models.Model):
    STATUS = [("Is Taken", "Is Taken"),
              ("Queue", "Queue")]


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    courier = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True, related_name="requests") #Кур'єр
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS, max_length=40, default = "Queue")

    def __str__(self):
        if self.status == "Is Taken":
            return f"{self.user}`s cart was taken by {self.courier} at {self.created}"
        else:
            return f"{self.user}`s cart is waiting for courier from {self.created}"

