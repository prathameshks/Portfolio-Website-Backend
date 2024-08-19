from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import webanalytics.settings as settings
from requests import get as ReqGet
from api.models import Visitor
# from api.serializers import VisitorSerializer


# Create your views here.
class defaultView(APIView):
    def get(self, request):
        return self.post(request)

    def post(self, request):
        ip_add = request.META.get("REMOTE_ADDR")
        resp = {'type' : 'POST'}
        
        resp['time'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        resp['ip_address'] = ip_add
        resp['ip_info'] = ReqGet(f"http://ip-api.com/json/{ip_add}?fields=status,message,continent,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,isp,org,as,mobile,proxy,query",timeout=5).json()
        resp['screen_resolution'] = request.data.get("screen_resolution")
        resp['referrer'] = request.data.get("referrer")
        resp['timezone'] = request.data.get("timezone")
        resp['language'] = request.data.get("language")
        resp['url'] = request.data.get("url")
        resp['user_agent'] = request.headers.get("User-Agent")
        resp['origin'] = request.headers.get("Origin")
        resp['Sec-Ch-Ua'] = request.headers.get("Sec-Ch-Ua")
        resp['Sec-Ch-Ua-Platform'] = request.headers.get("Sec-Ch-Ua-Platform")
        resp['Sec-Ch-Ua-Mobile'] = request.headers.get("Sec-Ch-Ua-Mobile")

        Visitor.objects.create(
            ip_address = ip_add,
            ip_info = resp['ip_info'],
            screen_resolution = resp['screen_resolution'],
            timezone = resp['timezone'],
            language = resp['language'],
            url = resp['url'],
            user_agent = resp['user_agent'],
            Sec_Ch_Ua = resp['Sec-Ch-Ua'],
            Sec_Ch_Ua_Platform = resp['Sec-Ch-Ua-Platform'],
            Sec_Ch_Ua_Mobile = resp['Sec-Ch-Ua-Mobile'],
        )        

        if(settings.DEBUG):
            return Response(resp,status= status.HTTP_200_OK)
        return Response("Connection Successful.",status= status.HTTP_200_OK)