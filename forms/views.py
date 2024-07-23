from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import webanalytics.settings as settings
from requests import get as ReqGet
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from forms.models import Contact,Testimonial
from api.models import Visitor
from forms.serializers import ContactSerializer,TestimonialSerializer
from api.serializers import VisitorSerializer

# Create your views here.
class ContactView(APIView):
    def get(self, request):
        return Response("Invalid Request.",status= status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        resp = {'success' : False,'ok':False}
        
        # get id of visitor object to store contact
        # visitor_id = request.session['visitor_id']
        
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            
            params = {
                'name': instance.name,
                'email': instance.email,
                'message': f"Thank You for your efforts to fill valuable feedback about '{instance.subject}' and help us to improve. We will get back to you soon.",
                'linkedin_link': 'https://www.linkedin.com/in/prathamesh-sable/',
                'facebook_link': 'https://www.facebook.com/prathamesh.sable.2003/',
                'twitter_link': 'https://twitter.com/pratham_sable/',
                'instagram_link': 'https://www.instagram.com/prathamesh.ks/',
            }
            subject = 'Thank you for your valuable feedback!'
            html_content = render_to_string('email_thanks.html', params)
            # html_content = get_template('email_event_reg.html').render(params)
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(
                subject,
                text_content,
                from_email='prathameshsable623@gmail.com',
                to=[instance.email],
                reply_to=['prathameshks2003@gmail.com'],
            )
            msg.attach_alternative(html_content, "text/html")
            
            # admin mail
            msg2 = EmailMultiAlternatives(
                "New Feedback - " + str(instance.subject),
                "Details of new feedback: \n\nName: " + instance.name + "\nEmail: " + instance.email + "\nSubject: " + instance.subject + "\nMessage: " + instance.message,
                from_email='prathameshsable623@gmail.com',
                to=['prathameshks2003@gmail.com'],
                reply_to=['prathameshks2003@gmail.com'],
            )
            
            try:
                msg.send()
                msg2.send()
            except Exception as e:
                print("mail not sent")
                print(e)
            resp['success'] = True
            resp['ok'] = True
            return Response(resp, status = status.HTTP_200_OK)
        else:
            # print(serializer.errors)
            return Response(resp,status=status.HTTP_400_BAD_REQUEST)
        
class TestimonialView(APIView):
    def get(self, request):
        return Response("Invalid Request.",status= status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = TestimonialSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            email_message = "Thank You for your valuable feedback!, Hope you experience was good, I will Look Your Message and try to Improve."
            
            match (instance.rating):
                case 1:
                    email_message = "Thank You for your valuable feedback!,Sorry for Bad Experience, I will work on the message you given and try to better the experience."
                case 2:
                    email_message = "Thank You for your valuable feedback!,Sorry for Bad Experience, I will work on the message you given and try to better the experience."
                case 3:
                    email_message = "Thank You for your valuable feedback!,Sorry for Bad Experience, I will work on the message you given and try to better the experience."
                case 4:
                    email_message = "Thank You for your valuable feedback!,Hope your experience is good, I will work on the message you given and try to Improve."
                case 5:
                    email_message = "Thank You for your valuable feedback!, Hope you experience was good, I will Look Your Message and try to Improve."
            
            params = {
                'name': instance.name,
                'email': instance.email,
                'message': email_message,
                'linkedin_link': 'https://www.linkedin.com/in/prathamesh-sable/',
                'facebook_link': 'https://www.facebook.com/prathamesh.sable.2003/',
                'twitter_link': 'https://twitter.com/pratham_sable/',
                'instagram_link': 'https://www.instagram.com/prathamesh.ks/',
            }
            
            subject = 'Thank you for your valuable Testimonial!'
            html_content = render_to_string('email_thanks.html', params)
            # html_content = get_template('email_event_reg.html').render(params)
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(
                subject,
                text_content,
                from_email='prathameshsable623@gmail.com',
                to=[instance.email],
                reply_to=['prathameshks2003@gmail.com'],
            )
            msg.attach_alternative(html_content, "text/html")
            
            # admin mail
            msg2 = EmailMultiAlternatives(
                "Received a new Testimonial!",
                "Details of new Testimonial: \n\nName: " + instance.name + "\nEmail: " + instance.email + "\nMessage: " + instance.message + "\nRating: " + str(instance.rating),
                from_email='prathameshsable623@gmail.com',
                to=['prathameshks2003@gmail.com'],
                reply_to=['prathameshks2003@gmail.com'],
            )
            
            try:
                msg.send()
                msg2.send()
            except Exception as e:
                print("mail not sent")
                print(e)            
            
            resp = {'success' : True,'ok':True}
            return Response(resp, status = status.HTTP_200_OK)
        else:
            # print(serializer.errors)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)