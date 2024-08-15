# from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# import webanalytics.settings as settings
# from requests import get as ReqGet
# from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
# from django.template.loader import get_template
from django.utils.html import strip_tags
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from django.utils import timezone
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

# from forms.models import Contact,Testimonial
# from api.models import Visitor
from forms.serializers import ContactSerializer,TestimonialSerializer
# from api.serializers import VisitorSerializer

# logging
import logging

# recaptcha
from webanalytics.recaptcha import verify_recaptcha

logger = logging.getLogger('webanalytics')

@method_decorator(ratelimit(key='ip', rate='1/m', method='POST'), name='post')
class ContactView(APIView):
    def get(self, request):
        logger.warning("Got a GET request for Contact Form, Which is not expected.")
        return Response("Invalid Request.",status= status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        resp = {'success' : False,'ok':False,'message':'Failed To Submit The Form.'}
        
        recaptcha_token = request.data.get('g-recaptcha-response')
        # print(f"{recaptcha_token = }")
        # print(request.data)
        
        if not recaptcha_token:
            resp['message'] = "Please verify CAPTCHA before submitting."
            logger.warning("Contact Form submission failed (No CAPTCHA).")
            return Response(resp,status=status.HTTP_400_BAD_REQUEST)
            
        
        is_valid_recaptcha = verify_recaptcha(recaptcha_token)
        
        if not is_valid_recaptcha:
            resp['message'] = "Failed To verify CAPTCHA."
            logger.warning("Contact Form submission failed (Invalid CAPTCHA).")
            return Response(resp,status=status.HTTP_400_BAD_REQUEST)
        
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
                # logger.info(f"Contact Form Email sent successfully to {instance.email}.")
            except Exception as e:
                logger.error(f"Contact Form Error sending email to {instance.email}: {e}")
                print("mail not sent")
                print(e)
            resp['success'] = True
            resp['ok'] = True
            resp['message'] = "Form Submitted Successfully."
            # logger.info(f"Contact Form submitted successfully by {instance.email}.")
            return Response(resp, status = status.HTTP_200_OK)
        else:
            # print(serializer.errors)
            logger.warning(f"Contact Form submission failed (Invalid Serializer): {serializer.errors}.")
            return Response(resp,status=status.HTTP_400_BAD_REQUEST)
        

@method_decorator(ratelimit(key='ip', rate='1/m', method='POST'), name='post')
class TestimonialView(APIView):
    def get(self, request):
        logger.warning("Got a GET request for Testimonial Form, Which is not expected.")
        return Response("Invalid Request.",status= status.HTTP_400_BAD_REQUEST)

    def post(self, request):        
        resp = {'success' : False,'ok':False,'message':'Invalid Request.'}
        
        recaptcha_token = request.data.get('g-recaptcha-response')
        # print(f"{recaptcha_token = }")
        # print(request.data)
        
        if not recaptcha_token:
            resp['message'] = "Please verify CAPTCHA before submitting."
            logger.warning("Contact Form submission failed (No CAPTCHA).")
            return Response(resp,status=status.HTTP_400_BAD_REQUEST)
            
        
        is_valid_recaptcha = verify_recaptcha(recaptcha_token)
        
        if not is_valid_recaptcha:
            resp['message'] = "Failed To verify CAPTCHA."
            logger.warning("Contact Form submission failed (Invalid CAPTCHA).")
            return Response(resp,status=status.HTTP_400_BAD_REQUEST)
        
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
                # logger.info(f"Testimonial Form Email sent successfully to {instance.email}.")
            except Exception as e:
                logger.error(f"Testimonial Form Error sending email to {instance.email}: {e}")
                print("mail not sent")   
            
            resp['success'] = True
            resp['ok'] = True
            resp['message'] = "Thank you for your valuable feedback!"
            # logger.info(f"Testimonial Form submitted successfully by {instance.email}.")
            return Response(resp, status = status.HTTP_200_OK)
        else:
            # print(serializer.errors)
            logger.warning(f"Testimonial Form submission failed (Invalid Serializer): {serializer.errors}.")
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)