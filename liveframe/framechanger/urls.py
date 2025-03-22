from django.urls import path

# from .views import *
from liveframe import consumers
from django.conf import settings
from django.conf.urls.static import static
from framechanger import views


# urlpatterns = [
#     path('generate-qr/<int:media_id>/', views.generate_qr, name='generate_qr'),
#     path('media/<int:media_id>/', views.media_detail, name='media_detail'),
#     path('client-signup', views.client_signup, name='client-signup'),
#     path('enterotp', views.otp, name='enterotp'),
#     path('client-password', views.client_signup_password, name='client-password'),
#     path('client-form', views.client_form, name='client-form'),
#     path('signin', views.client_signin, name='signin'),
#     path('dashboard', views.user_dashboard, name='dashboard'),
#     path('customer-data/<int:id>', views.customer_data, name='customer-data'),
    
# ]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = [

    
#     path("", views.video_page, name="index"),
#     path('camera_feed/', views.camera_feed, name='camera_feed'),  # Processed grayscale feed
#     path('video_page/', views.video_page, name='video_page'),  # Main page
#     path('video_feed/', camera_feed, name='video_feed'),
#     # path('', views.camera_page, name='camera_page'),
#     # path('video_feed/', consumers.VideoStreamConsumer.as_asgi()),
#     path('video_feed/', views.video_feed, name='video_feed'),
    
# ]


from django.urls import path
from .views import *

urlpatterns = [
    path('qr/userex/<int:userid>', views.camera_feed, name='camera_feed'),
    path('qr/<int:frameuserid>', views.generate_qr, name='qr'),
    path('', views.landing_page, name='landing_page'),
    path('contactus', views.contactus, name='contactus'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('tnc', views.tnc, name='tnc'),
    path('client-signup', views.client_signup, name='client-signup'),
    path('enterotp', views.otp, name='enterotp'),
    path('client-password', views.client_signup_password, name='client-password'),
    path('client-form', views.client_form, name='client-form'),
    path('signin', views.client_signin, name='signin'),
    path('dashboard', views.user_dashboard, name='dashboard'),
    path('customer-data/<int:id>', views.customer_data, name='customer-data'),
    path('customer-data/<int:id>', views.user_dashboard_search, name='customer-data'),
    path('add-frame/<int:id>', views.add_frame, name='add-frame'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path("payment",views.payment, name='payment'),
    path("logout/", user_logout, name="logout"),
]
