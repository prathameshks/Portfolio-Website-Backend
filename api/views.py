from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import webanalytics.settings as settings


# Create your views here.
class defaultView(APIView):
    def get(self, request):
        if(settings.DEBUG):
            resp = {
                'headers' : request.headers,
                'data' : request.data,
                'type' : 'GET',
                'time' : datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
            return Response(resp,status= status.HTTP_200_OK)
        else:
            return Response("Connection Successful.",status= status.HTTP_200_OK)
    
    def post(self, request):
        if(settings.DEBUG):
            resp = {
                'headers' : request.headers,
                'data' : request.data,
                'type' : 'POST',
                'time' : datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
            return Response(resp,status= status.HTTP_200_OK)
        else:
            return Response("Connection Successful.",status= status.HTTP_200_OK)