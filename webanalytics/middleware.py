import logging
import json
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('webanalytics')  # Use the logger name from the configuration

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Log the request
        log_data = {
            'method': request.method,
            'path': request.path,
            'user': str(request.user),
            'ip': self.get_client_ip(request),
        }
        logger.info(f"Incoming request: {json.dumps(log_data)}")

    def process_response(self, request, response):
        # Log the response
        log_data = {
            'method': request.method,
            'path': request.path,
            'status': response.status_code,
        }
        logger.info(f"Outgoing response: {json.dumps(log_data)}")
        return response

    def process_exception(self, request, exception):
        # Log the exception
        logger.error(f"Exception in {request.method} {request.path}: {str(exception)}", exc_info=True)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip