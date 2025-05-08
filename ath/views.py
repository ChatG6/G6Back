from django.http import HttpResponsePermanentRedirect,JsonResponse
from django.urls import reverse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from ath.serializers import check_password_validity
from django.views.decorators.csrf import csrf_exempt
from bd.settings import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.conf import settings
import resend
import random
import string



# Class-based view for user login
class LoginProc(APIView):
    @csrf_exempt
    def post(self, request):
        print(request.data)
        try:
            usr = request.data['usr']
            pwd = request.data['pwd']
            user = authenticate(username=usr, password=pwd)
            if user is not None:
                login(request, user)
                return Response({"details":"Logged in Succesfully"},status=status.HTTP_200_OK)
            else:
                return Response({"details":"Login Failed"},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class Verify(APIView):
    @csrf_exempt
    def post(self, request):
        print(request.data)
        try:
            usr = request.data['usr']
            user = User.objects.get(username=usr)
            email = user.email
            # Generate a random verification code
            length = 6
            verification_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
            resend.api_key = "re_2PdPD2Z7_P22aWom7f9YiPwEtJLFZBfuU"
             # Prepare the email content
            email_content = f"Your verification code is: {verification_code}"
            params = {
           "from": "ma <koora@chatg6.ai>",
             "to": [email],
            "subject": "hello world",
              "html": email_content,
                      }

            email = resend.Emails.send(params)
            print(email)
            return JsonResponse({'message': 'Verification email sent.'})
        except:
              return JsonResponse({'error': 'Failed to send verification email.'}, status=500)
# Class-based view for user registration
class SignUpProcView(APIView):
  @csrf_exempt
  def post(self,request):
    try:
        usr = request.data['usr']
        email = request.data['email']
        pwd = request.data['pwd']
        cpwd = request.data['cpwd']
        if User.objects.filter(email=email).exists():
              return Response({"details":"Email is already taken"},status=status.HTTP_226_IM_USED)
        elif User.objects.filter(username=usr).exists():
                    return Response({"details":"Username is already taken"},status=status.HTTP_226_IM_USED)
        elif check_password_validity(pwd) != 'Valid' :
                    val = check_password_validity(pwd)
                    val = val[2:len(val)-2]
                    errs = val.split("','")
                    errs = " ".join(errs)
                    return Response({'details':errs},status=status.HTTP_103_EARLY_HINTS)
        elif not usr.isalnum():
                    return Response({"details":"Username must be Alpha-numeric"},status=status.HTTP_103_EARLY_HINTS)
        elif (pwd!=cpwd):
              return Response({"details":"Passwords did not match"},status=status.HTTP_103_EARLY_HINTS)
        else:
            user = User.objects.create_user(username=usr,email=email,password=pwd)
            user.save()
            #send_email(usr,email)
            return Response({"details": "Account created successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
            print(e)
            print(User.objects)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#log_out process
def logout_proc(request):
  logout(request)
  return Response({"details":"User logged out"},status=status.HTTP_200_OK)

def message(viewName:str,msg:str) -> HttpResponsePermanentRedirect:
  return redirect(reverse(viewName) + '?message=' + msg)




