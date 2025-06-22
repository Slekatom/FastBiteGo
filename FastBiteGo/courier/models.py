from django.db import models
from accounts.models import CustomUser
from cart.models import Cart
User = CustomUser

class Request(models.Model):
    STATUS = [("Is Taken", "Is Taken"), # courier takes request at first
              ("Queue", "Queue")]
    # TAKEN_STATUS = [("Not Taken", "Not Taken"), # courier takes meal in real life
    #                 ("Taken", "Taken")]
    # FINISH_STATUS = [("Finished", "Finished"),
    #                  ("Not Finished", "Not Finished")]


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts1")
    courier = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True, related_name="requests1") #Кур'єр
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS, max_length=40, default = "Queue")
    # is_finished = models.CharField(choices=FINISH_STATUS, max_length=40, default="Not Finished")
    # is_taken = models.CharField(choices=TAKEN_STATUS, max_length=40, default="Not Taken")

    def __str__(self):
        if self.status == "Is Taken":
            return f"{self.user}`s cart was taken by {self.courier} at {self.created}"
        else:
            return f"{self.user}`s cart is waiting for courier from {self.created}"

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts2")
    courier = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="requests2")  # Кур'єр
    created = models.DateTimeField(auto_now=True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="chats3")

    def __str__(self):
        return f"{self.user} & {self.courier} chat"

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts4")
    text = models.TextField()
    created = models.DateTimeField(auto_now=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")

    def __str__(self):
        return f"{self.user} - {self.text}"

