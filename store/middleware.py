# middleware.py

from django.db import OperationalError
from django.http import HttpResponseServerError
import logging

class DatabaseErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, OperationalError):
            # Log the error for debugging purposes
            logging.error("Database connection error: %s", exception)
            # Return an HTTP 500 Server Error response with a user-friendly message
            return HttpResponseServerError("Database connection error. Please try again later.")
        return None
