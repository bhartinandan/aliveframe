from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.conf import settings
from framechanger.models import *
from framechanger import forms
from .utils import *
import qrcode
import os
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import razorpay
from django.contrib.auth import logout
from django.shortcuts import redirect


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# from .models import MediaData

# For web experience
@login_required
def generate_qr(request, frameuserid):
    print(frameuserid)
    # Generate QR code linking to the media URL
    media_url = request.build_absolute_uri(f'userex/{frameuserid}')
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(media_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


"""For app experience"""

# def generate_qr(request, media_id):
#     # Generate QR code linking to the media URL
#     media_url = request.build_absolute_uri(f'/media/{media_id}/')
#     qr = qrcode.QRCode(box_size=10, border=4)
#     qr.add_data(media_url)
#     qr.make(fit=True)

#     img = qr.make_image(fill_color="black", back_color="white")
#     response = HttpResponse(content_type="image/png")
#     img.save(response, "PNG")
#     return response

# def media_detail(request, media_id):
#     # Serve media details (image and video)
#     media = get_object_or_404(MediaData, id=media_id)
#     response_data = {
#         "title": media.title,
#         "image_url": request.build_absolute_uri(media.image.url),
#         "video_url": request.build_absolute_uri(media.video.url),
#     }
#     return JsonResponse(response_data)

@login_required
def user_dashboard(request):
    user = request.user
    print(user)
    client=ClientInfo.objects.filter(user=request.user.id).first()
    frameuser=FrameUserInfo.objects.filter(client_id=client).all()
    framecount=FrameCount.objects.filter(client_id=client).first()
    left_frame=0
    used_frame = 0
    total_frame=0
    if framecount:
        left_frame=framecount.frame_count
        used_frame = int(len(frameuser))
        total_frame=int(left_frame)+used_frame

    
    print(frameuser)
    data={'client':client,
          'frameuser':frameuser}

    return render(request,
                "user_dashboard.html",
                context={'client':client,
          'frameuser':frameuser,
          'framecount':framecount,
          'leftframe':left_frame,
          'usedframe':used_frame,
          'totalframe':total_frame
          })

@login_required
def user_dashboard_search(request, id):
    user = request.user
    print(user)
    client=ClientInfo.objects.filter(user=request.user.id).first()
    frameuser=FrameUserInfo.objects.filter(client_id=client).all()
    framecount=FrameCount.objects.filter(client_id=client).first()

    left_frame=framecount.frame_count
    used_frame = int(len(frameuser))
    total_frame=int(left_frame)+used_frame
    
    print(frameuser)
    data={'client':client,
          'frameuser':frameuser}

    return render(request,
                "user_dashboard.html",
                context={'client':client,
          'frameuser':frameuser,
          'framecount':framecount,
          'leftframe':left_frame,
          'usedframe':used_frame,
          'totalframe':total_frame
          })

@login_required
def customer_data(request,id):
    frameuser=FrameUserInfo.objects.filter(id=id).first()
    framemedia=MediaForWebExperience.objects.filter(user=frameuser).first()
    print("frame")
    print(framemedia)
    if request.method == "POST":
        framemedia.web_video=request.FILES.get('videoUpload')
        print(request.FILES.get('videoUpload'))
        framemedia.save()
    return render(request,
                "customer_details.html",
                context={'frameuser':frameuser,
                         'framemedia':framemedia
          })

def client_signup(request):
    try:
        message = ''
        if request.method == "POST":
            # form = forms.SignupuserForm(request.POST)
            user_id=request.POST.get('mobile')
            # user_id=form.cleaned_data['mobile']
            user_exists = User.objects.filter(username=user_id).first()
            if user_exists is not None:
                message = f'mobile number already exists!'
            else:
                data=token()
                request.session['user_id']=user_id
                request.session['token']=data["token"]
                response=send_phone_otp(user_id, data["token"])
                response_data=response["data"]
                if response["responseCode"]==200:
                    request.session['verificationId']=response_data["verificationId"]
                    return redirect("/enterotp")
                elif response["responseCode"]==506:
                    request.session['verificationId']=response_data["verificationId"]
                    return redirect("/enterotp")
                else:
                    message = f'Retry sending OTP'
        return render(request,
                    "client_signup.html",
                    context={
                    'message': message})
        
    except:
        return render(
            request, 'client_error.html')
    # if request.method == "POST":
    #     request.session['mobile'] = request.POST.get('mobile')
    #     return redirect("/enterotp")
    # return render(request,
    #             "client_signup.html")

def otp(request):
    # form = forms.UserotpForm()
    message = ''
    if request.method == "POST":
        # print("enter otp")
        # form = forms.UserotpForm(request.POST)
        message=""
        # print(form)
        # print(form.is_valid())
        # if form.is_valid():
        otp=request.POST.get('otp')
        # print(otp)
        user_id=request.session['user_id']
        token=request.session['token']
        verificationId=request.session['verificationId']
        print(user_id,token,verificationId)
        response=verify_otp(user_id,otp,verificationId,token)
        if response["responseCode"]==200:
            response_data=response["data"]
            request.session['verificationStatus']=response_data['verificationStatus']
            return redirect("/client-password")
        else:
            message="Wrong OTP Please enter correct OTP"
    return render(request,
                "client_otp.html",
                context={
                'message': message})
    
    # except:
    #     return render(
    #         request, 'client_error.html')

def client_signup_password(request):
    # form = forms.PasswordForm(request.POST)
    # if form.is_valid():
    if request.method == "POST":
        user_id=request.session['user_id']
        password=request.POST.get('password')
        if request.session['verificationStatus']=="VERIFICATION_COMPLETED":
            user = User.objects.create_user(username=user_id, password=password)
            user.save()
            user = authenticate(
                username=user_id,
                password=password,
            )
            if user is not None:
                login(request, user)
                # message = f'Hello {user.username}! You have been logged in'
                return redirect("/client-form")
                # return redirect('/dashboard')
            else:
                message = 'Invalid userId or password / Not registered, create new'
            return redirect("/client-form")
        
    return render(request,
                "client_password.html",context={})

@login_required
def client_form(request):
    usr=request.user

    if request.method == "POST":
        obj=ClientInfo()
        obj.user=usr
        obj.name = request.POST.get('name')
        obj.business_name = request.POST.get('businessname')
        obj.email = request.POST.get('emailid')
        obj.address = request.POST.get('address')
        obj.pin_code = request.POST.get('pincode')
        obj.city = request.POST.get('city')
        obj.contact = request.POST.get('contact')
        obj.state = request.POST.get('state')
        obj.country = request.POST.get('country')
        obj.save()
        return redirect("/dashboard")

    return render(request,
                "client_details.html")

def client_signin(request):
    try:
        # form = forms.LoginForm()
        message = ''
        if request.method == "POST":
            # form = forms.LoginForm(request.POST)
            # if form.is_valid():
            #     print(form.is_valid())
            user = authenticate(
                username=request.POST.get('mobile'),
                password=request.POST.get('password'),
            )
            
            if user is not None:
                login(request, user)
                message = f'Hello {user.username}! You have been logged in'
                return redirect('/dashboard')
            else:
                message = 'Invalid userId or password / Not registered, create new'
        return render(
            request, "client_signin.html",
            context={
                    'message': message})
    except:
        return render(
            request, 'client_error.html')
    
def user_logout(request):
    logout(request)
    return redirect("login")  # Redirect to the login page after logout
    
@login_required
def add_frame(request,id):
    usr=request.user
    cli_id=ClientInfo.objects.filter(id=id).first()

    if request.method == "POST":
        obj=FrameUserInfo()
        obj.name = request.POST.get('name')
        obj.email = request.POST.get('emailid')
        obj.address = request.POST.get('address')
        obj.pin_code = request.POST.get('pincode')
        obj.city = request.POST.get('city')
        obj.contact = request.POST.get('contact')
        obj.state = request.POST.get('state')
        obj.country = request.POST.get('country')
        obj.client_id = cli_id
        obj.save()
        obj1=MediaForWebExperience()
        obj1.user=obj
        obj1.web_video=request.FILES.get('videoUpload')
        obj1.save()
        return redirect("/dashboard")
    return render(request, 
                  "consumer_detail_form.html")

@login_required
def payment(request):
    # encoded_data = request.GET.get('data')
    # decoded_data = base64.b64decode(unquote(encoded_data)).decode('utf-8')
    # print("done")
    # print(decoded_data)
    framecount=10
    if request.method == "POST":
        framecount=int(request.POST.get('count'))
        request.session['framecount']=framecount
        amount = (framecount*99)*100  # Rs. amount in paisa
        request.session['fnl_amount']=amount
        currency = 'INR'
        print(framecount)

        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
        print(razorpay_order)
        return JsonResponse({
            "order_id": razorpay_order["id"],
            "amount": amount,
            "currency": "INR",
            "key": settings.RAZOR_KEY_ID,
        })

        # order id of newly created order.
        # razorpay_order_id = razorpay_order['id']
        # callback_url = 'paymenthandler/'

        # # we need to pass these details to frontend.
        # context = {}
        # context['razorpay_order_id'] = razorpay_order_id
        # context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        # context['razorpay_amount'] = amount
        # context['currency'] = currency
        # context['callback_url'] = callback_url

    return render(request,
                  "payment.html")

# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "GET":
        try:
            print("payment handler called")
            # get the required parameters from post request.
            payment_id = request.GET.get('payment_id')
            print(payment_id)
            razorpay_order_id = request.GET.get('order_id')
            print(razorpay_order_id)
            signature = request.GET.get('signature')
            print(signature)
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            print(result)
            if result is not None:
                amount = request.session['fnl_amount'] # Rs. 200
                try:
 
                    # capture the payemt
                    cap=razorpay_client.payment.capture(payment_id, amount)
                    print(cap)
 
                    # render success page on successful caputre of payment
                    # return render(request, 'c_paymentsuccess.html')
                    # response = order_placed(request.session['framecount'])
                    # return response
                    count=request.session['framecount']
                    usr=request.user
                    frameuser = ClientInfo.objects.filter(user=usr).first()
                    framecount = FrameCount.objects.filter(client_id=frameuser).first()
                    if framecount:
                        count_var=framecount.frame_count
                        framecount.frame_count=count_var+count
                        framecount.save()
                    else:
                        obj=FrameCount()
                        obj.client_id=frameuser
                        obj.frame_count=count
                        obj.save()

                    obj1=FramePayment()
                    obj1.client_id=frameuser
                    obj1.payment_status=True
                    obj1.payment_id=payment_id
                    obj1.razorpay_order_id=razorpay_order_id
                    obj1.amount=amount

                    response = redirect('/dashboard')
                    return response
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'c_paymentfailure.html')
            else:
 
                # if signature verification fails.
                return render(request, 'c_paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
    
def order_placed(request,count):
    print(count)
    usr=request.user
    frameuser = ClientInfo.objects.filter(user=usr).first()
    framecount = FrameCount.objects.filter(client_id=frameuser).first()
    if framecount:
        count_var=framecount.frame_count
        framecount.frame_count=count_var+count
        framecount.save()
    else:
        obj=FrameCount()
        obj.client_id=frameuser
        obj.frame_count=count
        obj.save()

    response = redirect('/dashboard')
    return response
































# from django.shortcuts import render

# # Create your views here.
# from django.http import HttpResponse


# from django.shortcuts import render

# def video_page(request):
#     return render(request, 'video_page.html')

# from django.shortcuts import render
# from django.http import StreamingHttpResponse
# import cv2
# import numpy as np


# def process_frame(frame):
#     """Apply modifications to the frame (e.g., add overlay or effects)."""
#     # Example: Convert to grayscale (replace with actual processing logic)
#     processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_GRAY2BGR)
#     return processed_frame


# def video_feed():
#     """Stream processed video frames to the browser."""
#     cap = cv2.VideoCapture(0)  # 0 to use the system's webcam
#     if not cap.isOpened():
#         raise RuntimeError("Error: Unable to access webcam!")

#     try:
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             # Process the frame
#             processed_frame = process_frame(frame)

#             # Encode frame as JPEG
#             _, buffer = cv2.imencode('.jpg', processed_frame)
#             frame = buffer.tobytes()

#             # Stream frame
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#     finally:
#         cap.release()
#         cv2.destroyAllWindows()


# def camera_feed(request):
#     """Django view to return the video feed."""
#     return StreamingHttpResponse(video_feed(), content_type='multipart/x-mixed-replace; boundary=frame')


# def camera_page(request):
#     """Render the camera feed page."""
#     return render(request, 'camera_page.html')



from django.shortcuts import render

def camera_feed(request, userid):
    # Frameuser = get_object_or_404(FrameUserInfo, consumer_unique_id=userid)
    frameuser = FrameUserInfo.objects.filter(id=userid).first()
    # Get the associated web video
    media = MediaForWebExperience.objects.filter(user=frameuser).first()

    print(media)

    if media and media.web_video:
        return render(request, 
                  "index2.html",
                  context={"media":media})
    else:
        return JsonResponse({"error": "No video found"}, status=404)
    

def landing_page(request,):
    return render(request, 
                  "index3.html")

def contactus(request):
    if request.method == "POST":
        obj=ContactForm()
        obj.name = request.POST.get('name')
        obj.business_name = request.POST.get('business')
        obj.email = request.POST.get('email')
        obj.contact = request.POST.get('contact')
        obj.message = request.POST.get('message')
        obj.save()
    return render(request, 
                  "Contactus.html")

def aboutus(request,):
    return render(request, 
                  "aboutus.html")

def tnc(request,):
    return render(request, 
                  "tnc.html")

def privacy_policy(request,):
    return render(request, 
                  "privacy_policy.html")






