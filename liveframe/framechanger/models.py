from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 
#web user experience
    
class ClientInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_date = models.DateTimeField(default=datetime.now, blank=True)
    name = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255)
    email = models.EmailField(max_length = 254)
    pin_code = models.CharField(max_length=6)
    address = models.TextField()
    contact = models.CharField(max_length=15)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)

    def __str__(self):
        return self.business_name
    
class FrameUserInfo(models.Model):
    date = models.DateTimeField(default=datetime.now, blank=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField(max_length = 254)
    contact = models.CharField(max_length=15)
    pin_code = models.CharField(max_length=6)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    client_id = models.ForeignKey(ClientInfo, on_delete=models.CASCADE, related_name='client')

    def __str__(self):
        return str(self.id)
    
class MediaForWebExperience(models.Model):
    user=models.ForeignKey(FrameUserInfo, on_delete=models.CASCADE, related_name='frameuser')
    web_video = models.FileField(upload_to='web_videos/')

    def __str__(self):
        return str(self.id)
    
class FrameCount(models.Model):
    client_id = models.ForeignKey(ClientInfo, on_delete=models.CASCADE, related_name='clientid')
    frame_count = models.IntegerField()

    def __str__(self):
        return str(self.id)
    
class FramePayment(models.Model):
    client_id = models.ForeignKey(ClientInfo, on_delete=models.CASCADE, related_name='clientassid')
    payment_status = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=30)
    razorpay_order_id = models.CharField(max_length=30)
    amount = models.IntegerField()
    paid_on = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.id)

class ContactForm(models.Model):
    name = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)
    email = models.EmailField(max_length = 254)
    message = models.CharField(max_length=500)

    def __str__(self):
        return str(self.id)




    




#App user experience

# class MediaData(models.Model):
#     title = models.CharField(max_length=255)
#     image = models.ImageField(upload_to='images/')
#     video = models.FileField(upload_to='videos/')

#     def __str__(self):
#         return str(self.id)

    
# class ClientInfo(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     client_unique_id = models.CharField(max_length=16, unique = True)
#     joined_date = models.DateTimeField(auto_now_add=True)
#     name = models.CharField(max_length=255)
#     business_name = models.CharField(max_length=255)
#     email = models.EmailField(max_length = 254)
#     pin_code = models.CharField(max_length=6)
#     address = models.TextField()
#     contact = models.CharField(max_length=15)
#     city = models.CharField(max_length=20)
#     state = models.CharField(max_length=20)
#     country = models.CharField(max_length=20)
#     image = models.ImageField(upload_to='profileimage/')

#     def __str__(self):
#         return self.business_name
    
# class FrameUserInfo(models.Model):
#     consumer_unique_id = models.CharField(max_length=16, unique = True)
#     date = models.DateTimeField(auto_now_add=True)
#     name = models.CharField(max_length=255)
#     address = models.TextField()
#     email = models.EmailField(max_length = 254)
#     contact = models.CharField(max_length=15)
#     city = models.CharField(max_length=20)
#     state = models.CharField(max_length=20)
#     country = models.CharField(max_length=20)
#     client_id = models.ForeignKey(ClientInfo, on_delete=models.CASCADE, related_name='client')
#     image = models.ImageField(upload_to='images/')
#     video = models.FileField(upload_to='videos/')

#     def __str__(self):
#         return self.user.username
    


