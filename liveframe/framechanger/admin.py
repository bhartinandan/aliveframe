from django.contrib import admin
from .models import *
# Register your models here.

#web user
admin.site.register(ClientInfo)
admin.site.register(FrameUserInfo)
admin.site.register(MediaForWebExperience)
admin.site.register(ContactForm)
admin.site.register(FrameCount)
admin.site.register(FramePayment)




#App user
# admin.site.register(MediaData)
# admin.site.register(ClientInfo)
# admin.site.register(FrameUserInfo)


